# AI Prompt Injection Detection Kit

## Threat Overview

**Prompt injection** is a technique where an attacker manipulates the input to a language model in a way that alters its behavior or output. This can lead to unauthorized access, data leakage, or other harmful actions. Prompt injection attacks exploit weaknesses in how LLMs process and interpret prompts.

### Real Examples
- In 2024, security researchers demonstrated prompt injection techniques that could trick an AI assistant into revealing internal documentation or bypassing access controls.
- Prompt injection has been used to manipulate AI systems in customer service chatbots, causing them to leak sensitive data or perform unintended actions.

### Who Is Exposed?
Organizations using LLM-based tools (chatbots, agents, assistants) for internal or customer-facing tasks are at risk. The threat is especially high when these systems lack input sanitization or safety checks.

## Countermeasure

This kit provides an **AI-assisted prompt injection detection system** that analyzes user inputs before they reach an LLM. It combines a rule-based filter with an LLM to detect potentially malicious prompts and flags them for review or rejection.

### How It Works
1. Input prompt is analyzed by a combination of:
   - Static rules (detecting common injection indicators)
   - An LLM endpoint (`LLM_URL`) that evaluates the input for safety.
2. If either detects a high risk, the input is flagged and can be rejected or reviewed.

### Running the Kit
Run the detection script with:
```bash
python3 detect_prompt_injection.py --input "Your prompt here"
```

To test:
```bash
python3 test_detect_prompt_injection.py
```

## Non-AI Controls

- Input sanitization: Remove or escape special characters from user input.
- Least privilege for agents: Limit what actions an AI assistant can perform.
- Human review: Have a human approve sensitive prompts before processing.
- Allow-lists: Only allow known safe inputs or commands.