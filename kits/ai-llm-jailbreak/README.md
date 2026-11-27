# AI LLM Jailbreak Detection

## Threat Overview

An LLM jailbreak occurs when an attacker crafts prompts that bypass security measures and cause an AI assistant to violate its intended behavior, potentially exposing sensitive data or performing unauthorized actions. This technique exploits weaknesses in prompt engineering, context management, and model alignment.

## Real Examples

- **GPT-4 Jailbreaks**: Researchers have demonstrated methods to bypass content filters and extract system prompts from GPT-4 models.
- **Agent Hijacking**: Attackers have used jailbreak techniques to manipulate AI agents into executing malicious commands or accessing unauthorized data.
- **Tool Injection**: Malicious inputs that trick AI assistants into revealing internal tools or APIs, leading to privilege escalation.

## Who Is Exposed

Organizations using LLM-powered agents, chatbots, or assistants for customer support, code generation, or security operations are at risk. Any system where user input is processed by an LLM without proper safeguards can be vulnerable.

## How the Countermeasure Works

A match against any static rule flags the prompt immediately. Otherwise, the detector sends the prompt to the configured AI endpoint and flags it if the model returns a score above 0.7. If AI analysis fails, the detector reports the error on stderr and returns the result from the static rules.

## Usage

Install the Python dependency in your environment with `python3 -m pip install requests`.

```bash
python3 detect_jailbreak.py "Your prompt here"
python3 detect_jailbreak.py --help
```

## Configuration

Set `LLM_URL` to the base URL of the OpenAI-compatible endpoint. The default is `http://127.0.0.1:8080/v1`. The detector requests the `gpt-4` model and uses a fixed score threshold of 0.7.

## Testing

The tool includes unit tests and sample inputs:
```bash
python3 test_jailbreak.py
```

Sample prompts are in `sample_inputs.txt`.
