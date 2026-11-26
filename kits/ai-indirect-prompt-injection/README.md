# AI Indirect Prompt Injection Triage

## Threat Overview

**Indirect prompt injection** is a technique where attackers exploit vulnerabilities in AI systems through external inputs, such as web pages, documents, or tool descriptions. Unlike direct prompt injection (where the attacker directly manipulates an LLM's input), indirect injection occurs when an LLM interacts with external components that are not properly sanitized, leading to unintended behavior.

### Key Examples

- **Tool Descriptions**: An attacker injects malicious instructions into a tool's description that gets used by an AI agent.
- **Web Content**: A phishing website or malicious document can be processed by an AI system and result in unauthorized actions.
- **Agent Inputs**: Malicious inputs from external systems (e.g., APIs) can be interpreted by an AI agent as legitimate commands.

### Who is Exposed?

Organizations using AI agents or LLMs that interact with external data sources, tools, or documents are at risk. This includes:

- AI-powered customer service chatbots
- Agents that use external tools or APIs
- Systems processing untrusted documents or web content

## Countermeasure

This kit provides a triage script that evaluates inputs for signs of indirect prompt injection attempts. It uses an LLM to assist in detection but can also function with rule-based checks alone.

### How It Works

1. **Input Analysis**: The script analyzes user prompts, tool descriptions, or external content for suspicious patterns.
2. **AI Assistance**: If an LLM endpoint is available, it uses the model for deeper analysis.
3. **Rule-Based Fallback**: In case of no AI response, the system defaults to known heuristics and patterns.
4. **Output Guard**: Prevents any malicious or unauthorized output from being generated.

## Non-AI Controls

- **Input Sanitization**: Ensure all external inputs are properly sanitized before processing.
- **Tool Description Validation**: Validate tool descriptions and ensure they are not tampered with.
- **Least Privilege for Agents**: Limit the permissions of AI agents to reduce impact if an injection occurs.
- **Human Approval**: Require human review of critical agent actions.

## Usage

```bash
python3 triage.py "input text here"
```
