#!/usr/bin/env python3
"""Triage outbound inference requests without sending their contents to the reviewer."""

import argparse
import json
import os
import re
import sys
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEFAULT_LLM_URL = "http://127.0.0.1:8080/v1"
PATTERNS = {
    "private_key_marker": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "credential_assignment": r"\b(?:api[_ -]?key|password|access[_ -]?token)\s*[:=]\s*\S{4,}",
    "email_address": r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b",
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def model_review(features):
    base = os.getenv("LLM_URL", DEFAULT_LLM_URL).rstrip("/")
    try:
        endpoint = urlsplit(base)
        if endpoint.scheme not in {"http", "https"} or endpoint.hostname not in {"127.0.0.1", "::1"}:
            return "unavailable"
        if endpoint.username or endpoint.password or endpoint.query or endpoint.fragment:
            return "unavailable"
        payload = {
            "model": os.getenv("LLM_MODEL", "local-reviewer"),
            "messages": [
                {"role": "system", "content": "Review inference routing metadata. Reply REVIEW if the request merits human review given the destination approval, asserted retention setting, declared data classification and local indicators. Otherwise reply NO_ADDITIONAL_SIGNAL. An asserted retention setting is not proof of compliance."},
                {"role": "user", "content": json.dumps(features)},
            ],
        }
        request = Request(base + "/chat/completions", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with build_opener(NoRedirect()).open(request, timeout=3) as response:
            result = json.loads(response.read(65536))
        label = result["choices"][0]["message"]["content"].strip()
        return {"REVIEW": "review", "NO_ADDITIONAL_SIGNAL": "no_additional_signal"}.get(label, "unavailable")
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
        return "unavailable"


def assess(prompt, *, approved, classification, retention, rules_only=False):
    indicators = [name for name, pattern in PATTERNS.items() if re.search(pattern, prompt, re.IGNORECASE)]
    features = {
        "destination_approved": approved,
        "classification": classification,
        "retention": retention,
        "indicators": indicators,
    }
    reasons = list(indicators)
    if not approved:
        reasons.append("destination_not_approved")
    if classification != "public":
        reasons.append("classification_requires_review")
    if retention != "zero-retention-asserted":
        reasons.append("retention_requires_review")
    model = "disabled" if rules_only else model_review(features)
    if model == "review":
        reasons.append("model_requested_review")
    return {"verdict": "review" if reasons else "no_signal", "reasons": reasons, "model": model}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-destination", action="store_true", help="Set only after matching the routed endpoint to your allow-list")
    parser.add_argument("--classification", choices=["public", "internal", "restricted", "unknown"], default="unknown")
    parser.add_argument("--retention", choices=["zero-retention-asserted", "retained", "unknown"], default="unknown")
    parser.add_argument("--rules-only", action="store_true")
    args = parser.parse_args()
    result = assess(sys.stdin.read(), approved=args.approved_destination, classification=args.classification, retention=args.retention, rules_only=args.rules_only)
    print(json.dumps(result))
    return 1 if result["verdict"] == "review" else 0


if __name__ == "__main__":
    sys.exit(main())
