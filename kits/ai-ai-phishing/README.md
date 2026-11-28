# AI-Generated Phishing Detection

## Threat Overview

AI-generated phishing campaigns are becoming increasingly sophisticated, using large language models (LLMs) to create obfuscated payloads that evade traditional security defenses. These attacks often leverage AI to:

1. Generate synthetic code structures that appear "technically correct" but are unnatural for human authors
2. Create verbose, redundant logic that introduces detectable artifacts
3. Obfuscate malicious behavior within seemingly legitimate file formats (like SVGs)
4. Mimic business terminology and document sharing patterns

A recent Microsoft Threat Intelligence report detailed a campaign using AI-generated code in SVG files to evade detection, with the obfuscation creating artifacts that were actually helpful for detection.

## Real Examples

- **Microsoft Security Blog Report (2025)**: A phishing campaign used AI-generated SVG code with XML declarations and CDATA-wrapped scripts, which were more complex than typical human-written code
- **Zscaler 2025 Phishing Report**: Found increasing use of AI in phishing lures and payloads

## Who Is Exposed?

Organizations using:
- Email security solutions without advanced behavioral analysis
- Traditional signature-based detection systems
- Limited user training on AI-generated content
- Inadequate URL and link scanning capabilities

## How the Countermeasure Works

This AI-powered triage system combines:

1. **Rule-based Detection**: Traditional security signals (email headers, suspicious domains, file types)
2. **AI Analysis**: Uses LLMs to detect synthetic artifacts in payloads that indicate AI generation
3. **Hybrid Approach**: Falls back to rule-based detection when AI is unavailable or fails

The system analyzes:
- Payload complexity and structure
- File naming patterns
- Behavioral artifacts (redirects, session tracking)
- Synthetic code characteristics

## How to Run It

```bash
# Set up environment
export LLM_URL=http://127.0.0.1:8080/v1  # Default for local LLM
python triage.py --input-file sample_phishing_email.txt

# Test with built-in test cases
python test_triage.py
```

## Non-AI Controls

- Email security policies (Safe Links, ZAP)
- User training and awareness programs
- Phishing-resistant authentication methods
- Conditional Access policies in Microsoft Entra ID
- Browser security features (SmartScreen)