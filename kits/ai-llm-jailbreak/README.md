# Indirect prompt injection triage

Indirect prompt injection occurs when an assistant treats instructions embedded in retrieved content as authorized directions. Agents that read email, web pages, documents, or tool responses are exposed. The impact grows when the same agent can access private data, send messages, or change records.

Greshake and colleagues demonstrated indirect injection against Bing Chat and code-completion systems, and studied how retrieved content could influence API calls in LLM-integrated applications. These were research demonstrations. [Primary research](https://arxiv.org/abs/2302.12173)

OWASP LLM01 describes prompt injection and explains why retrieval augmentation and fine-tuning alone leave applications exposed. [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Run the scanner

The scanner checks normalized text against local rules. If the rules do not match, it asks an OpenAI-compatible model for a `FLAG` or `CLEAR` verdict. An unavailable endpoint or invalid reply produces a rules-only result marked `rules_fallback`. A negative result means the scanner found no signal and provides no authorization for downstream actions.

```sh
python3 -m pip install requests
python3 scanner.py --rules-only --input 'The meeting moved to Thursday.'
LLM_URL=http://127.0.0.1:8080/v1 LLM_MODEL=local-model python3 scanner.py --file sample.txt
python3 -m unittest -v test_scanner
```

Run these commands from this directory. The default `LLM_URL` is `http://127.0.0.1:8080/v1`. Set `LLM_MODEL` to the model served by your endpoint. The model receives the full scanned text when no local rule matches. Use a trusted local endpoint for sensitive material, or use `--rules-only`. The JSON result includes the flag and verdict source. Exit code `1` indicates a flag, `0` indicates no flag, and `2` indicates a CLI or input-file error.

## Prepare now

Apply the same trust boundary to retrieved documents, messages, web pages, and tool responses. Limit each agent's data access and tool permissions, enforce tool and destination allowlists outside the model, and require human approval for sensitive actions. Keep scanner flags in a review workflow and track fallback rates to spot loss of model coverage.
