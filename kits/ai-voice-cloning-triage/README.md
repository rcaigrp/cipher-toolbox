# AI Voice Cloning Triage

## Threat Overview

**AI voice cloning scams** are a growing concern where cybercriminals use artificial intelligence to replicate the voices of trusted individuals (family members, colleagues, or public figures) to deceive victims into transferring money or sharing sensitive information.

### Key Examples

- A scammer calls a victim pretending to be their child in distress, requesting urgent financial help.
- An AI-generated voice impersonates a senior executive to authorize a wire transfer.
- Fraudsters use cloned voices to gain access to secure accounts by mimicking authorized users.

### Who is Exposed?

Anyone who uses voice-based communication systems or financial services, especially those with limited digital literacy or who are not aware of the risks associated with AI-generated audio content.

## Countermeasure

The script scans transcripts or typed messages for phrases associated with scams, such as urgent requests for money. It uses case-insensitive text matching. It does not analyze audio or verify a caller’s identity.

`MALICIOUS` means a phrase matched. `SAFE` means no listed phrase matched. Either result can occur in a legitimate or fraudulent call. Verify unexpected requests by contacting the person through a number you already know.

### How to Run

Run the script with:
```bash
python3 triage.py
```

Enter one message at a time. Type `quit` or close standard input to exit. To process a file, pass its path as shown below. Each nonblank line is checked separately.

## Sample Input File

A sample input file (`sample_inputs.txt`) is included to demonstrate usage:
```bash
python3 triage.py sample_inputs.txt
```

## Testing

Run tests with:
```bash
python3 test_triage.py
```
