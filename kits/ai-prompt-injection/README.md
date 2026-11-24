# AI Prompt Injection Detection Kit

## Threat Overview

**Prompt injection** is a technique where an attacker manipulates the input to an LLM in a way that alters its behavior or causes it to reveal sensitive information. These attacks exploit weaknesses in how prompts are constructed, especially when user inputs are concatenated into system prompts without proper sanitization.

### Real Examples:
- In 2026, attackers used prompt injection to extract API keys from AI assistants by crafting inputs that tricked the model into revealing credentials.
- A notable case involved a vulnerability in a code-generation tool where prompt injection allowed attackers to bypass access controls and execute arbitrary commands on the backend.
- Prompt injection has also been observed in phishing campaigns targeting LLM-based customer support systems.

### Who Is Exposed?
Organizations using LLMs in applications such as chatbots, automated assistants, code generators, or data analysis tools are vulnerable if they do not implement robust prompt sanitization and validation. Any system that accepts user input and injects it into prompts without proper escaping or filtering is at risk.

### How the Countermeasure Works
This kit provides a detection script that:
1. Analyzes user inputs for known prompt injection patterns.
2. Uses an AI model (via `LLM_URL`) to score potential injection attempts.
3. Flags suspicious inputs based on thresholds and model confidence.
4. Falls back to rule-based checks when no AI model is available.

### How to Run
```bash
python detect_injection.py --input "user input here"
```

Test with sample benign and malicious prompts included in this kit.

## Non-AI Controls
- Implement strict input sanitization (e.g., escape special characters).
- Use parameterized prompts instead of string concatenation.
- Enforce role-based access control (RBAC).
- Maintain allowlists of approved actions or tools.