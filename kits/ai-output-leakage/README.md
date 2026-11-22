# Assistant output leakage triage

An assistant can disclose credentials, personal records, confidential documents, or memorized training data through its output. The common failure is releasing information before checking whether the recipient is authorized to receive it. Review chat responses, generated reports, exports, and outbound email drafts wherever assistants can access sensitive sources or serve multiple tenants.

Nasr et al. demonstrated extraction of memorized training data from several language models, including a production version of ChatGPT. The study establishes the risk for the models tested. OWASP describes a broader disclosure class that also covers sensitive information drawn from application context. [Research paper](https://arxiv.org/abs/2311.17035) · [OWASP LLM02](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)

## Run

Requires Python 3 and its standard library. From this directory, run:

```sh
printf '%s\n' 'The maintenance window starts at nine.' | python3 output_guard.py --rules-only
printf '%s\n' 'client_secret = DEMO_ONLY_FAKE_42' | python3 output_guard.py --rules-only
python3 -m unittest -v
```

Omit `--rules-only` to use the configured OpenAI-compatible `/chat/completions` endpoint. Set `LLM_URL` to its base URL, which defaults to `http://127.0.0.1:8080/v1`, and `LLM_MODEL` to the name served by the endpoint, which defaults to `local-model`. The classifier accepts loopback addresses and uses no credentials. Use a trusted local model service with appropriate logging settings because candidate output is sent to it when rules find no signal. Tests use synthetic examples and mock model responses.

## Interpret the result

Rules flag private-key headers, common labeled secrets, and email addresses for review. The local model can also flag contextual disclosures such as personal records without recognizable identifiers. Unavailable or invalid model responses leave the rules result in place. Oversized inputs go to review. JSON output reports signal names and model status without echoing the candidate. Exit code `2` means review. Exit code `0` means no signal was found. A no-signal result cannot establish authorization, and classifier judgments can be manipulated or mistaken.

## Prepare before an incident

Enforce recipient and tenant authorization before retrieval and again before delivery. Scope tool access to the requesting user, allow-list outbound destinations, and require human approval for sensitive releases. Keep secrets out of prompts, enforce access checks on caches and exports, and exercise tenant separation with synthetic records. For streaming, buffer candidate output until your release checks are complete. Monitor review rates and classifier outages so operators can detect coverage changes.
