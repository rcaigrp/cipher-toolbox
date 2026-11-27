# AI Prompt Injection Detection Kit

## Threat Overview

**Prompt injection** occurs when user inputs are crafted to manipulate an LLM's behavior, potentially bypassing safety constraints or causing unintended actions. Unlike traditional software vulnerabilities, prompt injection can be subtle and may not be visible to human users but is still parsed by the model.

### Real Examples
- In 2025, attackers used prompt injection to compromise enterprise AI assistants, extracting confidential data.
- Indirect prompt injection attacks exploited web forms and document processing systems to inject malicious prompts into LLM workflows.

### Who Is Exposed?
Organizations that integrate LLMs into applications (chatbots, agents, RAG systems) are at risk. Any system where user input directly affects model prompts is vulnerable, especially those without input sanitization or prompt engineering safeguards.

## Countermeasure

This kit provides an **AI-assisted prompt injection detection system** that analyzes user inputs before they reach an LLM. It combines rule-based checks with AI classification to identify potentially malicious prompts.

### How It Works
1. Input prompt is analyzed by a combination of:
   - Static rules (detecting common prompt injection indicators)
   - An LLM endpoint (`LLM_URL`) that evaluates the input for safety.
2. If either detects a high risk, the input is flagged and can be rejected or reviewed.

### Running the Kit
Run the detection script with:
```bash
python detect_prompt_injection.py --input "user prompt here"
```

Ensure `LLM_URL` environment variable points to an OpenAI-compatible endpoint (default: `http://127.0.0.1:8080/v1`).

## Non-AI Controls
- Input sanitization and validation
- Least privilege access for LLM agents
- Human approval workflows for sensitive actions
- Allow-listing of known safe prompts