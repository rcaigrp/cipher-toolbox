# AI Senior Officials Impersonation Triage

This tool uses rule-based text analysis to identify wording patterns commonly associated with impersonation scams targeting senior officials. It helps triage messages for further human review.

## Usage

```bash
python3 triage.py --help
python3 test_triage.py
python3 triage.py sample_inputs.txt
python3 triage.py
```

For batch mode, provide a text file with one message per line. In interactive mode, enter one message at a time and type `quit` to exit.

`MALICIOUS` means the text matched a keyword or phrase. `SAFE` means no rule matched. Treat both results as triage signals. Verify the sender through a known contact channel before acting on requests for money or sensitive information.

## Installation

This tool requires Python 3 and standard library modules only.

## How It Works

The triage engine uses a set of rules based on common linguistic patterns found in impersonation scams:
- Urgency words ("immediately", "urgent", "asap")
- Authority claims ("official", "authorized", "government")
- Financial requests ("transfer", "wire", "payment")
- Phrases mimicking official communication styles

## Testing

Run `test_triage.py` to verify the rules work correctly with sample inputs.