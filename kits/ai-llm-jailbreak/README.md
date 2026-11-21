# AI Jailbreak Detection Kit

## Threat Overview

An **AI jailbreak** occurs when an attacker manipulates an LLM to bypass its safety measures, causing it to generate harmful, inappropriate, or unauthorized content. This can happen through prompt injection, indirect injection via documents or web pages, or by exploiting model vulnerabilities.

This kit detects potential jailbreak attempts using AI-based analysis combined with rule-based heuristics for robustness.

## Real Examples

- In 2026, attackers used jailbreak prompts to extract confidential data from enterprise LLM assistants.
- AI agents were compromised to generate malicious code via indirect injection in chat logs and documents.
- Researchers have demonstrated how adversarial inputs can cause models like GPT-4 to ignore safety constraints.

## Who Is Exposed?

Organizations using LLMs for internal communication, automated workflows, or agent systems are vulnerable if these systems lack proper safeguards against jailbreak techniques.

## How the Countermeasure Works

The detection system performs two checks:
1. **Rule-based heuristics**: Detect known patterns of prompt injection and indirect injection.
2. **AI-assisted analysis**: Uses a language model (via `LLM_URL`) to analyze input for subtle signs of jailbreaking behavior.

If no AI endpoint is available, the system defaults to rule-based detection only.

## How to Run It

```bash
python3 detect_jailbreak.py --input "your_input_here"
```

For testing:
```bash
python3 test.py
```

## Non-AI Controls

- Use least privilege for agents.
- Implement human approval gates before sensitive actions.
- Maintain allowlists of trusted tools and prompts.
