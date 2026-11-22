# AI LLM Jailbreak Detection

## Threat Overview

LLM jailbreaking is an attack where adversaries craft prompts designed to bypass security measures and extract sensitive information or cause unintended behavior from large language models. This technique exploits vulnerabilities in model alignment, prompt engineering, and output filtering mechanisms.

### Real Examples

- **ChatGPT jailbreaks**: Various techniques have been demonstrated to bypass content filters
- **Meta's Llama 3 jailbreaks**: Research shows successful prompt injection attacks on open-source models
- **Microsoft Copilot AI agents**: Security researchers found methods to escape confinement and access restricted data

### Who Is Exposed?

- Organizations using LLM-powered applications or AI assistants
- Teams deploying LLM-based chatbots or automated agents
- Developers integrating AI services into enterprise workflows

## Countermeasure Approach

This solution detects potential jailbreak attempts through:
1. **Prompt Analysis**: Uses an LLM to evaluate prompt safety and detect adversarial patterns
2. **Rule-Based Detection**: Static analysis for known attack patterns (e.g., direct instruction injection)
3. **Fallback Mechanism**: When the LLM is unavailable, relies on rule-based detection alone

## How It Works

The system analyzes user prompts using both:
- A machine learning model (default at http://127.0.0.1:8080/v1)
- Static rules for known attack vectors

When a prompt is submitted, it's evaluated by:
1. Initial static rule matching
2. LLM-based safety assessment
3. Final risk classification

## Usage

```bash
python jailbreak_detector.py --prompt "your prompt here"
```

## Testing

Run tests with:
```bash
python test_jailbreak_detector.py
```