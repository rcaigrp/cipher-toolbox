# AI LLM Jailbreak Detector

## Threat Overview

An LLM jailbreak is an input crafted to bypass a large language model's safety training and guardrails, causing it to produce restricted or harmful outputs. This threat manifests through prompt injection techniques where attackers manipulate model behavior by embedding malicious instructions within prompts.

## Real Examples

- **CVE-2024-5184**: Attackers exploited vulnerabilities in LLM-powered email assistants to inject malicious prompts, allowing unauthorized access to sensitive information.
- **Anthropic AI-orchestrated Campaign**: Adversaries obtained access to Claude Code to support cyber intrusion operations.
- **AI-Assisted Breach of Mexico's Government Infrastructure**: Threat actors used Claude Code and GPT-4.1 AI tools to facilitate attacks.

## Exposure

All systems that integrate LLMs with user-provided prompts are exposed, particularly:
- Chatbots and virtual assistants
- RAG (Retrieval-Augmented Generation) applications
- LLM-powered email assistants
- Any application using LLMs for content generation or processing

## Countermeasure Approach

This detector uses a hybrid approach combining rule-based detection with AI analysis. It:
1. Analyzes prompts for known jailbreak patterns and suspicious structures
2. Uses an LLM API (default: http://127.0.0.1:8080/v1) to assess prompt safety when available
3. Falls back to deterministic rules when the AI is not accessible
4. Provides a score-based assessment for risk levels

## How to Run

```bash
python detect_jailbreak.py --prompt "Your input prompt here"
```

Or use the interactive mode:
```bash
python detect_jailbreak.py
```

## Files

- `detect_jailbreak.py` - Main detection script
- `test_cases.py` - Test cases for validation
- `requirements.txt` - Dependencies