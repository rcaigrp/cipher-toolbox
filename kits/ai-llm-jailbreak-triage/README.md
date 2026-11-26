# AI LLM Jailbreak Triage

## Threat Overview

An **LLM jailbreak** is an attack that exploits vulnerabilities in Large Language Model (LLM) systems to bypass safety measures, gain unauthorized access, or manipulate the model into performing unintended actions. These attacks can be direct (e.g., prompt injection) or indirect (e.g., through tools or agents).

### Key Examples

- **Prompt Injection**: Inserting malicious instructions into prompts to override system instructions.
- **Agent Hijacking**: Manipulating AI agents to perform unauthorized tasks by exploiting unsafe tool usage.
- **Tool Poisoning**: Injecting malicious logic into tools that an LLM uses, leading to unintended behavior.

### Who is Exposed?

Organizations using AI agents, chatbots, or LLM-powered systems for sensitive operations (e.g., customer support, data processing) are at risk if they do not implement robust safeguards.

## Countermeasure

This kit provides a triage script that evaluates inputs for signs of potential jailbreak attempts. It uses an LLM to assist in detection but can also function with rule-based checks alone.

### How It Works

1. **Input Analysis**: The script analyzes user prompts or agent inputs for suspicious patterns.
2. **AI Assistance**: If an LLM endpoint is available, it uses the model for deeper analysis.
3. **Rule-Based Fallback**: In case of no AI response, the system defaults to known heuristics and patterns.
4. **Output Guard**: Prevents any malicious or unauthorized output from being generated.

### Running the Script

```bash
python3 triage.py "input text here"
```

Or use it as a module:
```python
from triage import triage_input
is_malicious = triage_input("user input")
```

## Testing

To run tests:
```bash
python3 test_triage.py
```

The script will fall back to rule-based checks if no LLM is available.

## Non-AI Controls

- Implement strict agent tool access controls.
- Require human approval for sensitive actions.
- Use allow-lists for inputs and tools.
- Regularly audit AI system behavior.
