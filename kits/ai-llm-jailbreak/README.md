# AI Jailbreak Detection Kit

## Threat Overview

An **LLM jailbreak** occurs when an attacker manipulates an LLM to bypass its safety measures, constraints, or intended behavior. These attacks exploit weaknesses in the model's training, prompt engineering, or output filtering systems.

### Real Examples:
- In 2026, multiple AI agents were compromised via prompt injection that allowed attackers to extract confidential data.
- Researchers demonstrated jailbreak techniques using adversarial prompts to make models generate harmful content despite safety protocols.
- A known technique involves "role-playing" prompts that trick the model into acting as a different persona or bypassing restrictions.

### Who Is Exposed?
Organizations deploying LLMs in production environments (e.g., chatbots, code assistants, customer service agents) are vulnerable if they do not implement proper safeguards. Any system where user input is processed by an LLM without validation risks exposure.

### How the Countermeasure Works
This kit provides a detection script that:
1. Analyzes input prompts for known jailbreak patterns.
2. Uses an AI model (via `LLM_URL`) to score potential jailbreak attempts.
3. Flags suspicious inputs based on thresholds and model confidence.
4. Falls back to rule-based checks when no AI model is available.

### How to Run
```bash
python detect_jailbreak.py --input "prompt text here"
```

Test with sample benign and malicious prompts included in this kit.

## Non-AI Controls
- Implement strict input sanitization.
- Enforce role-based access control (RBAC).
- Use human review for critical decisions.
- Maintain allowlists of approved actions or tools.
