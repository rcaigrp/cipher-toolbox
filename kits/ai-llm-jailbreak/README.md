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
2. **AI Scoring (Optional)**: If `LLM_URL` is set, send the prompt to a model trained to detect jailbreaks and score it on a scale from 0 to 1.
3. **Decision Logic**:
   - A rule match alone triggers a `True` result.
   - A rule match with a low model score (e.g., < 0.3) can clear the flag.
   - A high model score (> `JAILBREAK_THRESHOLD`) triggers a `True` result.

### Configuration

- `LLM_URL`: The endpoint for an OpenAI-compatible LLM (default: `http://127.0.0.1:8080/v1`).
- `JAILBREAK_THRESHOLD`: Threshold for AI model scores to classify as jailbreaks (default: 0.7).
- `MODEL_NAME`: Model identifier used in the request (default: `jailbreak-detector`).

The model is only invoked when:
- A rule-based match is detected, OR
- The input exceeds 500 characters.

### Testing

Run tests with `python3 detect_jailbreak.py --test`.

## Implementation Details

The detector uses regular expressions to identify known jailbreak indicators. When a prompt matches one or more of these patterns, the system flags it as potentially malicious. Optionally, a machine learning model can be used for more nuanced detection.

### Non-AI Controls

- **Least Privilege**: Ensure AI agents operate with minimal required permissions.
- **Human Approval**: For critical actions, require manual confirmation.
- **Allow Lists**: Restrict access to known good prompts or commands.