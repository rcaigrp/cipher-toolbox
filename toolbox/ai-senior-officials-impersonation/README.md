# AI Senior Officials Impersonation Triage

Use this rule-based text triage tool to flag wording associated with impersonation scams for human review. The [implementation, tests, and sample data](../../kits/ai-senior-officials-impersonation/) live in the companion kit.

## Usage

From the repository root, run the following commands.

```bash
cd kits/ai-senior-officials-impersonation
python3 triage.py --help
python3 test_triage.py
python3 triage.py sample_inputs.txt
python3 triage.py
```

For batch mode, replace `sample_inputs.txt` with a text file containing one message per line. In interactive mode, enter one message at a time and type `quit` to exit.

`MALICIOUS` means the text matched a keyword or phrase. `SAFE` means no rule matched. Treat both results as triage signals. Verify the sender through a known contact channel before acting on requests for money or sensitive information.
