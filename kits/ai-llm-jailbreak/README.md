# AI Jailbreak Detection Kit

## Threat Overview

An **LLM jailbreak** occurs when an attacker manipulates a language model to bypass its safety constraints, causing it to generate harmful content or perform unauthorized actions. These attacks exploit weaknesses in the model's alignment and safety mechanisms.

### Real Examples
- In 2026, researchers demonstrated jailbreak techniques that could cause LLMs to ignore safety rules, including generating malicious code or inappropriate content.
- AI assistants used in enterprise environments have been compromised through prompt injection and jailbreak prompts, leading to data leaks and unauthorized access.

### Who Is Exposed?
Organizations using LLM-based tools (chatbots, agents, assistants) for internal or customer-facing tasks are at risk. The threat is especially high when these systems lack input sanitization or safety checks.

## Countermeasure

This kit provides an **AI-assisted jailbreak detection system** that analyzes user inputs before they reach an LLM. It combines a rule-based filter with an LLM to detect potentially malicious prompts and flags them for review or rejection.

### How It Works
1. Input prompt is analyzed by a combination of:
   - Static rules (detecting common jailbreak indicators)
   - An LLM endpoint (`LLM_URL`) that evaluates the input for safety.
2. If either detects a high risk, the input is flagged and can be rejected or reviewed.

### Running the Kit
Run the detection script with:
```bash
python detect_jailbreak.py --input "user prompt here"
```

Ensure `LLM_URL` environment variable points to an OpenAI-compatible endpoint (default: `http://127.0.0.1:8080/v1`).

## Non-AI Controls
- Human review of flagged inputs
- Agent input allow-lists
- Least privilege access for LLM agents
