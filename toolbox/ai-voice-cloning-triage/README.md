# AI Voice Cloning Triage

## Overview

This tool is a defensive mechanism designed to identify potential AI voice cloning scams. It helps security teams triage incoming voice communications for signs of impersonation or fraud.

### Key Features

- **Rule-based detection** for common voice cloning patterns.
- **Sample test cases** included to validate the triage logic.
- **Interactive and batch modes** for flexibility in usage.

## How It Works

1. The tool checks input prompts against a list of known voice cloning indicators.
2. If a match is found, it flags the communication as potentially malicious.
3. The result is a binary classification: `MALICIOUS` or `SAFE`.

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

- Enforce strict verification procedures for financial transactions.
- Educate staff on recognizing voice cloning scams.
- Implement codewords or personal questions as additional layers of authentication.

This kit helps teams prepare for AI-related threats by providing a proactive defense mechanism against voice cloning fraud.