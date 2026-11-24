# AI LLM Injection Defense

## Threat

LLM injection occurs when an attacker manipulates prompts or inputs to an AI system in a way that leads to unintended behavior, such as bypassing safety controls, accessing unauthorized data, or influencing the AI's output. This can happen through direct prompt injection (e.g., inserting malicious instructions), indirect injection via documents or agent tools, or by exploiting vulnerabilities in how AI systems process external inputs.

## Real Examples

- In 2025, attackers used prompt injection to manipulate a customer service chatbot into revealing internal documentation.
- A phishing campaign used LLM-generated messages that bypassed content filters by exploiting injection techniques.
- In another case, an AI assistant was tricked into sharing confidential user data through carefully crafted prompts.

## Who Is Exposed

- Organizations using LLM-powered assistants (chatbots, agents, tools).
- Users who interact with untrusted or compromised AI systems.
- Developers integrating LLMs without proper input sanitization or guardrails.

## How the Countermeasure Works

This kit provides a **prompt validation and anomaly detection system** that:
1. Analyzes user prompts for suspicious patterns (e.g., instruction injection, role reversal).
2. Uses an LLM to classify whether a prompt is potentially malicious.
3. Applies rules-based checks when no LLM is available.
4. Logs flagged inputs for review or blocking.

It's designed to be **pluggable**—you can use it with any OpenAI-compatible endpoint (default: `http://127.0.0.1:8080/v1`) or fall back to rule-based detection alone.

## How to Run It

```bash
python3 detect_injection.py --input "test prompt here"
```

To test, run:
```bash
python3 test.py
```

## Non-AI Controls

- **Least privilege for agents**: Limit what tools or data each AI agent can access.
- **Human approval**: Require manual review of flagged inputs before action.
- **Allow-lists**: Only permit known-safe prompts or inputs to pass through.
