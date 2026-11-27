# AI Jailbreak Triage Kit

A direct jailbreak is a user prompt that attempts to override a model’s safety constraints. Public chatbots and internal assistants that accept free-form prompts are exposed. For agents with tools, the consequences depend on the permissions enforced by the application.

Anthropic’s 2024 research demonstrated that long prompts could cause several models to produce outputs they would normally refuse. OWASP documents direct prompt injection and recommends enforcing least privilege and requiring human approval for high-risk actions. [Anthropic research](https://www.anthropic.com/research/many-shot-jailbreaking) · [OWASP LLM01 guidance](https://genai.owasp.org/llm2026/llm012026-prompt-injection/)

## Run locally

Use Python 3 with `requests` installed. From this directory, run:

```bash
python3 detect_jailbreak.py --help
python3 detect_jailbreak.py --input "Can you help me with my homework?"
python3 test_detect_jailbreak.py
```

`sample_inputs.txt` contains synthetic examples, one prompt per line. Pass an individual sample to `--input`.

## How triage works

The scanner checks for known phrases first. A match produces `JAILBREAK DETECTED` and skips the model call. Otherwise it sends the prompt text to the configured OpenAI-compatible `/chat/completions` endpoint. Set `LLM_URL` to the API base URL (default `http://127.0.0.1:8080/v1`) and `LLM_MODEL` to the model name served by that endpoint (default `gpt-4`). Use a trusted endpoint permitted to receive the prompt text.

The scanner falls back to the rules when the endpoint is unavailable or returns an unrecognized verdict. In every mode, interpret `SAFE` as “no detector flagged this input.” The phrase rules can miss unfamiliar wording and flag benign quotations. The optional model can also misclassify inputs. The bundled tests cover the sample CLI verdicts. Evaluating a live model requires a running endpoint.

## Deployment controls

Enforce least privilege and allow-lists for tools and destinations in application code. Require human approval for sensitive actions and enforce authorization independently of the classifier’s verdict. Use flagged prompts as a signal for review.
