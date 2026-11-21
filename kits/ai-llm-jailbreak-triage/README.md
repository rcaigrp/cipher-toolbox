# AI LLM Jailbreak Triage

## Threat Overview

LLM jailbreak attacks exploit vulnerabilities in large language model (LLM) prompt handling by injecting malicious instructions that bypass safety filters and cause the model to behave in unintended ways. These attacks can lead to data leakage, unauthorized actions, or system compromise.

The most durable patterns include:
1. Persona hijacking
2. Prefix injection with refusal suppression
3. Encoding and ASCII-art obfuscation
4. Multi-turn escalation
5. Authority override (Skeleton Key)
6. Policy-file framing
7. Stacked combinations

## Real Examples

- **2025 ArXiv Study**: Demonstrated prompt injection attacks on ChatGPT via user inputs, web retrieval, and system-level agent instructions.
- **Security Boulevard Report**: Detailed how untrusted content can be injected into prompts to manipulate model behavior.

## Who is Exposed

Organizations using LLMs in:
- Chatbots
- Agentic workflows
- RAG (Retrieval-Augmented Generation)
- Automated decision-making systems

## How the Countermeasure Works

The triage tool uses an AI-based classifier to detect prompt injection attempts by analyzing input prompts for known jailbreak patterns and suspicious structures. It works alongside traditional signature-based detection and rule enforcement.

## How to Run

1. Set up the environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install openai
   ```

2. Configure `LLM_URL` (default: http://127.0.0.1:8080/v1)

3. Run tests:
   ```bash
   python triage.py test
   ```

## Non-AI Controls

- Least privilege for agents and tools
- Human approval for risky actions
- Allow-lists for tool permissions
- Explicit instruction hierarchy design
- Content isolation and labeling