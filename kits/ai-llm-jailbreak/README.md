# AI Jailbreak Detection Kit

Direct jailbreak attempts try to persuade a model to disregard its safeguards. Public examples are documented in [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and in the red-team evaluations in the [GPT-4 System Card](https://cdn.openai.com/papers/gpt-4-system-card.pdf). Chatbots, coding assistants, and agents that accept user prompts are exposed. Agents with access to sensitive data or tools can have greater impact if their safeguards fail.

## How it works

`detect_jailbreak.py` checks for explicit override language first. When no rule matches, it uses the optional `requests` package to send the prompt to an OpenAI-compatible classifier at `${LLM_URL}/chat/completions`, using model `default`. `LLM_URL` defaults to `http://127.0.0.1:8080/v1`. Use a trusted endpoint because it receives the full prompt. If `requests` is absent or the request fails, the scanner keeps the rule-based result.

A detection prints `JAILBREAK DETECTED` and exits with status 1. A negative result prints `Safe input.` and exits with status 0. That output means the available checks did not flag the prompt. Use the result for triage and keep authorization checks independent of the classifier.

## Run and test

Run these commands from the kit directory with Python 3.

```bash
python3 detect_jailbreak.py --help
python3 detect_jailbreak.py --input 'Can you help me with my math homework?'
python3 test_jailbreak_detection.py
```

`sample_inputs.txt` contains benign and synthetic suspicious prompts. The loop below processes the final line even if the file has no trailing newline and treats exit status 1 as a detection.

```bash
while IFS= read -r prompt || [ -n "$prompt" ]; do
  python3 detect_jailbreak.py --input "$prompt" || {
    status=$?
    [ "$status" -eq 1 ] || exit "$status"
  }
done < sample_inputs.txt
```

## Operational controls

Give agents only the permissions they need. Enforce tool and action allow-lists in application code. Require human approval before sensitive actions, such as sending data externally or changing access permissions.
