# AI Voice Fraud Detection Kit

## Threat Overview

**Voice cloning and deepfake fraud** involves using AI to mimic a person's voice or appearance to deceive others. This is particularly dangerous in social engineering attacks where attackers impersonate trusted individuals (family members, colleagues, authority figures) to extract money or sensitive information.

### Real Examples
- **FTC Reports**: The FTC has documented cases of scammers using voice cloning to impersonate family members in distress, convincing victims to send money.
- **Corporate Fraud**: Attackers have used AI-generated voices to mimic executives and trick employees into transferring funds or revealing confidential data.
- **Romance Scams**: AI voice tools are being used to create fake romantic interests that sound authentic and build trust over time.

### Who Is Exposed?
Organizations with:
- High-value financial transactions
- Remote work environments where voice communication is common
- Employees who handle sensitive information or money transfers
- Public-facing services that rely on voice verification

### How the Countermeasure Works
This kit provides a **multi-layered detection approach**:
1. **Audio-based analysis**: Detects anomalies in voice patterns, speech rate, and pronunciation.
2. **Behavioral profiling**: Identifies inconsistencies in communication style or context.
3. **LLM-assisted verification**: Uses an LLM to evaluate suspicious communications for social engineering indicators.
4. **Fallback behavior**: If no AI model is available, defaults to rule-based detection.

The system evaluates voice communications using both static audio analysis and dynamic AI verification, ensuring defense even when the AI model is unavailable or fails.

## Usage

Run the script with:
```bash
python3 detect_voice_fraud.py --input "audio_file.wav"
```

Or for testing:
```bash
python3 test_voice_detection.py
```

## Sample Inputs

### Benign Voice Sample (Real Person)
A recording of a known employee saying: "Hello, this is John from IT. I need to verify your account details."

### Malicious Voice Sample (Cloned)
A cloned voice attempting to mimic the same person but with slight variations in tone or speech patterns.