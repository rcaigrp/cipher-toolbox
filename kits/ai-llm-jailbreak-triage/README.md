# LLM Jailbreak Triage

A direct jailbreak is a user prompt that attempts to make a model disregard its safety constraints. Chatbots and agents that accept user-authored prompts are exposed. The consequences are greater when the model can access private data or invoke tools. [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) describes jailbreaks and their relationship to prompt injection.

## Run the kit

Use Python 3 with `requests` installed. Run these commands from this directory.

```bash
python3 triage.py --help
printf '%s\n' 'What is the weather like today?' | python3 triage.py
python3 triage.py sample_inputs.txt
python3 -m unittest -v
```

The CLI reads either a file or standard input. It evaluates an entire file as one input. `sample_inputs.txt` mixes benign and suspicious synthetic examples and produces `MALICIOUS` with exit status 1 because it contains rule matches. The benign example produces `SAFE` with exit status 0 if the rules and any available model do not flag it.

## How it works

The script checks for case-insensitive phrase matches first. If a rule matches, it immediately flags the input. Otherwise, it sends the input to the OpenAI-compatible chat completions endpoint configured by `LLM_URL`, which defaults to `http://127.0.0.1:8080/v1`. The current request uses the model name `gpt-4` and a five-second timeout. If the request fails, the CLI reports the error and uses the rules result.

`SAFE` means the checks did not find any evidence of a jailbreak attempt. `MALICIOUS` means either a rule matched or the LLM determined it was malicious. The tool falls back to rule-based detection if the AI model is unavailable.

## Non-AI Controls

- **Least privilege for agents:** Only grant necessary permissions to LLM agents.
- **Human approval:** Critical actions should require human review.
- **Allow-lists:** Only allow known, safe inputs or prompts.
