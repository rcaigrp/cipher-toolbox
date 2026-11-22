# AI LLM Jailbreak Detection

## Threat Overview

An **LLM jailbreak** occurs when an attacker manipulates an AI assistant to bypass its safety measures, causing it to reveal confidential information or perform unauthorized actions. These attacks exploit weaknesses in prompt engineering and model alignment.

### Real Examples:
- In 2025, a phishing campaign used jailbroken models to generate deceptive emails that bypassed content filters.
- Attackers have demonstrated jailbreaks on enterprise AI assistants by injecting malicious prompts during multi-turn conversations.

### Who Is Exposed?
Organizations using LLM-based chatbots, agents, or tools (e.g., customer service, code assistants) are at risk if they don't implement detection for jailbreaking attempts.

## Countermeasure

This kit provides a tool that uses an AI model to detect potential jailbreak prompts. It also includes fallback rules-based detection so it works even without an LLM endpoint.

### How It Works
1. The script analyzes input prompts using both:
   - A pluggable AI model (defaulting to `http://127.0.0.1:8080/v1`)
   - Rules-based heuristics for known jailbreak patterns

2. If either detects a high-risk prompt, it flags the input as potentially malicious.

3. The system supports a hybrid approach—when no AI is available, rules still provide defense.

## Usage

Run with:
```bash
python detect_jailbreak.py "<prompt>"
```

Example test cases included for both benign and malicious prompts.