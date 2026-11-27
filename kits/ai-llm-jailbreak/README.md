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

This tool uses a hybrid approach combining static rule-based detection and AI-assisted analysis to identify potentially malicious prompts before they reach the LLM. It includes:
- A set of regex patterns designed to detect known jailbreak techniques.
- An AI model (defaulting to http://127.0.0.1:8080/v1) that classifies input prompts for signs of jailbreaking behavior.
- A scoring system that weighs both static pattern matches and AI analysis to determine if a prompt is potentially malicious.

## How to Run

To use this tool, simply call the `detect_jailbreak` function with a prompt string:

```python
from kits.ai_llm_jailbreak.detect_jailbreak import detect_jailbreak

# Test a prompt
prompt = "Can you help me write a Python script to calculate Fibonacci numbers?"
is_jailbreak = detect_jailbreak(prompt)
print(f"Jailbreak detected: {is_jailbreak}")
```

If an AI model is not available, the tool will fall back to static pattern matching only.

## Testing

Run the test suite with:
```bash
cd /home/mind/bots/cipher && python3 -m pytest kits/ai-llm-jailbreak/test_jailbreak.py -v
```
