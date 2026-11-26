# AI LLM Jailbreak Triage

## Overview

This tool is a defensive mechanism designed to identify potential LLM jailbreak attempts and prompt injection attacks. It can be used by security teams to triage inputs to AI systems, especially in environments where AI agents or chatbots are used.

### Key Features

- **Rule-based detection** for common jailbreak patterns.
- **AI-assisted analysis** using a configurable endpoint (e.g., local LLM).
- **Fallback behavior** when the AI is unavailable.
- **Sample test cases** included to validate the triage logic.

## How It Works

1. The tool checks input prompts against a list of known jailbreak patterns.
2. If an AI model is available, it queries the model for additional context.
3. If no AI response is received, it defaults to rule-based decisions.
4. The result is a binary classification: `MALICIOUS` or `SAFE`.

## Usage

Run the triage script with:
```bash
python triage.py <input_file>
```

Or interactively:
```bash
python triage.py
```

## Non-AI Controls

- Enforce least privilege for AI agents.
- Require human approval for critical actions.
- Maintain allowlists of trusted tools and commands.

## Threats Addressed

- Prompt injection attacks that attempt to bypass safety measures.
- Agent hijacking through unsafe tool usage.
- Tool poisoning in agent workflows.

This kit helps teams prepare for AI-related threats by providing a proactive defense mechanism against jailbreak attempts.