# AI LLM Jailbreak Detection

## Threat Overview

An LLM jailbreak occurs when an attacker bypasses the safety mechanisms and ethical constraints of a large language model, allowing it to generate harmful, inappropriate, or forbidden content. This can include generating hate speech, illegal advice, or other content that violates policies.

### Real Examples
- In 2026, a security researcher demonstrated how a simple prompt injection could bypass content filters in several commercial LLMs.
- A phishing campaign used jailbroken LLMs to generate convincing scam emails that evaded traditional spam filters.

### Who is Exposed?
Organizations using LLM APIs, chatbots, or AI assistants are exposed. Attackers can exploit these systems for malicious purposes such as generating phishing content, creating harmful misinformation, or extracting sensitive data.

## Countermeasure

This kit provides a detection mechanism to identify potential jailbreak attempts in input prompts. It uses an LLM-assisted approach with fallback rules to flag suspicious patterns that may indicate an attempt to circumvent safety measures.

### How it Works
1. **LLM-Based Analysis**: The system sends input prompts to an LLM endpoint for analysis.
2. **Rule-Based Fallback**: If the LLM is unavailable or returns an error, it falls back to predefined rules and heuristics.
3. **Scoring System**: Each prompt gets a score based on its likelihood of being a jailbreak attempt.

### Running the Countermeasure
```bash
python3 detect_jailbreak.py --input "prompt to analyze"
```

## Non-AI Controls
- Implement strict input validation and sanitization.
- Enforce human review for flagged inputs.
- Maintain allow-lists for known safe prompts.
- Regularly update and patch LLM models.