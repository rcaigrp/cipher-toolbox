# AI Senior Officials Impersonation Triage

## Overview

This tool is a defensive mechanism designed to identify potential AI-generated impersonation scams targeting senior US officials. It helps security teams triage incoming communications for signs of fraud.

### Key Features

- **Rule-based detection** for common impersonation patterns.
- **Sample test cases** included to validate the triage logic.
- **Interactive and batch modes** for flexibility in usage.

## How It Works

1. The tool checks input prompts against a list of known impersonation indicators.
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
- Educate staff on recognizing AI-generated impersonation attempts.
- Implement codewords or personal questions as additional layers of authentication.

This kit helps teams prepare for AI-related threats by providing a proactive defense mechanism against senior official impersonation scams.