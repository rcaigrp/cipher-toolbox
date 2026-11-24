# AI LLM Jailbreak Defense

## Threat

An LLM jailbreak occurs when an attacker manipulates prompts to bypass safety measures and extract confidential information or cause unintended behavior from an AI assistant. These attacks can be direct (e.g., prompt injection) or indirect (e.g., through documents, web pages, or agent tools).

## Real Examples

- In 2025, attackers used prompt injection to manipulate a financial advisor AI into revealing client data.
- A phishing campaign used LLM-generated messages that bypassed content filters by exploiting jailbreak techniques.

## Who Is Exposed

- Organizations using LLM-powered assistants (chatbots, agents, tools).
- Users who interact with untrusted or compromised AI systems.
- Developers integrating LLMs without proper input sanitization or guardrails.

## How the Countermeasure Works

This kit provides a **prompt validation and anomaly detection system** that:
1. Analyzes user prompts for suspicious patterns (e.g., instruction injection, role reversal).
2. Uses an LLM to classify whether a prompt is potentially malicious.
3. Applies rules-based checks when no LLM is available.
4. Logs flagged inputs for review or blocking.

It's designed to be **pluggable**—you can use it with any OpenAI-compatible endpoint (default: `http://127.0.0.1:8080/v1`) or fall back to rule-based detection alone.

## How to Run It

```bash
python3 detect_jailbreak.py --input "test prompt here"
```

To test, run:
```bash
python3 test.py
```

## Non-AI Controls

- Enforce least privilege for AI agents.
- Require human approval for sensitive actions.
- Maintain allowlists of trusted tools and data sources.

## Notes

The detection system will fall back to rule-based checks if the LLM endpoint is not available.