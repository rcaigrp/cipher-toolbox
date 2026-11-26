# AI Senior Officials Impersonation Triage

## Threat Overview

A malicious campaign has emerged where cybercriminals use AI-generated voice messages to impersonate senior US officials. These attacks are part of a broader trend involving **smishing** (SMS phishing) and **vishing** (voice phishing), aiming to gain unauthorized access to personal or official accounts.

### Key Examples

- A scammer sends a text message claiming to be from a high-ranking government official, requesting urgent financial assistance.
- An AI-generated voice message mimics a known official to persuade the recipient to click on a malicious link or provide sensitive information.

### Who is Exposed?

Individuals who are current or former senior US federal or state government officials, along with their contacts and associates. Anyone receiving suspicious messages from what appears to be a high-ranking official should be cautious.

## Countermeasure

This kit provides a triage script that evaluates incoming communications for signs of impersonation attempts by senior officials. It focuses on detecting unusual patterns in message content and behavior that may indicate fraud.

### How It Works

1. **Behavioral Analysis**: The script looks for red flags such as urgency, emotional manipulation, and unexpected financial requests.
2. **Verification Requests**: Suggests specific verification steps to ensure authenticity.
3. **Pattern Recognition**: Detects known phishing tactics used in AI-generated impersonation campaigns.

### How to Run

Run the script with:
```bash
python triage.py <input_file>
```

Or interactively by running:
```bash
python triage.py
```

## Sample Inputs

- **Benign Input:** "Hi, it's your colleague. I need to discuss a project update."
- **Malicious Input:** "I'm in urgent need of funds for an emergency. Please send $500 immediately."

## Non-AI Controls

- Enforce strict verification procedures for financial transactions.
- Educate staff on recognizing AI-generated impersonation attempts.
- Implement codewords or personal questions as additional layers of authentication.

This kit helps teams prepare for AI-related threats by providing a proactive defense mechanism against senior official impersonation scams.