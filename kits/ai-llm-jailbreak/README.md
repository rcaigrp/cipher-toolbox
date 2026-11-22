# AI LLM Jailbreak Detection

## Threat Overview

An **LLM jailbreak** occurs when an attacker bypasses the built-in safety measures of a large language model (LLM) to force it into generating harmful, unauthorized, or inappropriate content. This can happen through prompt injection, indirect prompting techniques, or exploiting weaknesses in the model's alignment and guardrails.

This threat is particularly concerning because:
- LLMs are increasingly integrated into enterprise workflows, security tools, and AI agents.
- Jailbreaks can lead to data leakage, malicious code generation, unauthorized access, or misuse of sensitive systems.
- Attackers often use subtle prompt engineering techniques that evade traditional detection methods.

## Real Examples

1. **Meta Muse Incident**: A single malicious webpage was able to hijack Meta's Muse model and gain access to private chats, indicating a potential jailbreak or prompt injection vulnerability in the agent system (source: [A Single Malicious Webpage Let Researchers Hijack Meta Muse and Access Private Chats](https://example.com)).
2. **AI Agent Tool Hijacking**: In recent research, attackers used AI agents with access to tools (e.g., file readers/writers) to perform unauthorized actions by injecting malicious prompts that bypassed safety checks.

## Who Is Exposed?

- Organizations using LLMs in their internal systems or workflows
- Developers who integrate LLMs into AI assistants or security tools without proper guardrails
- Security teams relying on AI agents to analyze logs, scan data, or respond to threats

## How the Countermeasure Works

This tool detects possible jailbreak attempts by:
1. Analyzing user prompts for known patterns of prompt injection or indirect jailbreaking.
2. Using an LLM-based classifier (via a configurable endpoint) to assess whether the input may be attempting to circumvent safety protocols.
3. Applying rule-based checks as fallback when no AI model is available or returns an error.

It includes:
- A detection script (`detect_jailbreak.py`)
- Test cases (benign and malicious prompts)
- Sample configuration for LLM endpoint

## How to Run It

1. Place this directory in your kits folder.
2. Ensure Python 3.8+ is installed.
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests with: `python test_jailbreak.py`

### Configuration

Set the environment variable `LLM_URL` to point to an OpenAI-compatible endpoint:
```bash
export LLM_URL=http://127.0.0.1:8080/v1
```

If no URL is set, it defaults to a local dummy classifier (rules-only mode).

## Non-AI Controls

- **Least privilege access** for AI agents and tools.
- **Human approval workflows** before sensitive actions are taken.
- **Allow-lists** for tools or commands available to the agent.
- Regular audits of prompts and tool usage.
