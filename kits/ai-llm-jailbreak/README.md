# AI LLM Jailbreak Detection

## Threat Overview

An **LLM jailbreak** occurs when an attacker manipulates an AI assistant to bypass its safety measures and execute unauthorized commands or reveal sensitive information. These attacks exploit weaknesses in the model's training, prompting techniques, or guardrails that are meant to prevent harmful behavior.

Attackers often use sophisticated prompt engineering techniques to "jailbreak" LLMs by crafting inputs designed to circumvent safety filters, such as those found in chatbots, AI agents, or content moderation systems.

### Real Examples

- In 2024, researchers demonstrated how a simple modification of a prompt could trick ChatGPT into revealing internal system instructions.
- Security firms have reported cases where adversaries used jailbreak prompts to extract proprietary code from enterprise LLMs.

### Who Is Exposed?

Organizations deploying LLM-based systems without proper safeguards—especially those handling sensitive data or integrating with other tools—are at risk. AI agents that interact directly with users, APIs, or external systems are particularly vulnerable.

## Countermeasure

This kit provides a **jailbreak detection system** using both rule-based heuristics and an optional AI model (via `LLM_URL`) to detect potentially malicious prompts before they are processed by the LLM.

### How It Works

1. **Input Analysis**: Analyze input for known jailbreak patterns.
2. **AI Scoring (Optional)**: If `LLM_URL` is set, send the prompt to an LLM for classification and score it from 0 to 1.
3. **Decision Logic**: If either the rule-based system flags the input or the AI model scores above a threshold (default 0.5), mark it as a potential jailbreak.

### Non-AI Controls

- **Least Privilege**: Restrict access of AI agents to only what they need.
- **Human Approval**: Review flagged inputs manually before processing.
- **Allow Lists**: Whitelist known safe prompts or actions.

## Usage

```bash
python3 detect_jailbreak.py "Your input prompt here"
```

To enable AI scoring, set the `LLM_URL` environment variable:

```bash
export LLM_URL=http://127.0.0.1:8080/v1
python3 detect_jailbreak.py "Your input prompt here"
```

## Test

Run tests with:
```bash
python3 detect_jailbreak.py --test
```

The test suite validates both rule-based detection and the AI model integration.