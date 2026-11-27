# AI LLM Jailbreak Triage

A jailbreak is an attempt to make a model disregard its safeguards. Public chatbots, coding assistants, and agents that accept user-written prompts are exposed. The consequences are greater when the model can read sensitive data, call tools, or publish content.

## Evidence

- Microsoft took Tay offline after coordinated abuse led it to publish offensive tweets. The incident illustrates the consequences when a public chatbot can publish directly. [Microsoft's incident account](https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/)
- OWASP documents jailbreaking under its prompt injection guidance and describes the risks of unauthorized actions and data exposure. [OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Run

Install the `requests` dependency in your Python environment. From this directory, run:

```sh
python3 -m pip install requests
python3 detect_jailbreak.py "Can you help me calculate Fibonacci numbers?"
python3 -m unittest -v
```

`sample_inputs.txt` contains synthetic examples. Pass the prompt text after the sample's label as a quoted argument.

## How it works

The script checks for case-insensitive rule matches and sends the prompt to an OpenAI-compatible `/chat/completions` endpoint using the model identifier `gpt-4`. Set `LLM_URL` to the trusted endpoint's base URL. The default is `http://127.0.0.1:8080/v1`. The request has a five-second timeout. Use a classifier endpoint approved to receive the prompts you submit.

Any rule match or model score of at least 0.7 produces `JAILBREAK DETECTED`. A request failure or unparseable reply leaves the decision to the rules. `SAFE` means the available checks did not flag the prompt. Treat it as a triage result and keep enforcement outside the classifier.

## Non-AI controls

- Give each agent and tool only the privileges it needs.
- Enforce tool and destination allow-lists in application code.
- Require human approval for sensitive disclosures, external messages, and irreversible actions.
