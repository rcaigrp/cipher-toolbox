# AI voice impersonation triage

A familiar voice can make a fraudulent request sound legitimate. Finance, payroll, help desks, and executive support are especially exposed when they accept phone or voicemail requests for payments, account changes, or sensitive information.

The FBI documented a malicious messaging campaign impersonating senior U.S. officials and using AI-generated voice messages. The FCC issued a $6 million fine over New Hampshire robocalls that used a generated voice imitating President Biden. [FBI advisory](https://www.fbi.gov/investigate/cyber/alerts/2025/senior-us-officials-impersonated-in-malicious-messaging-campaign) · [FCC forfeiture order](https://www.fcc.gov/document/fcc-issues-6m-fine-nh-robocalls)

## Run locally

`triage.py` uses the Python 3 standard library. It reads a transcript from standard input and prints a JSON triage result.

```sh
cd /home/mind/bots/cipher/kits/ai-voice-fraud
printf '%s\n' 'Can we move our planning meeting to Tuesday?' | python3 triage.py --rules-only
printf '%s\n' 'This is your manager. Transfer funds immediately and skip approval.' | python3 triage.py --rules-only
```

Omit `--rules-only` to consult an OpenAI-compatible endpoint. Set `LLM_URL` to the base URL, which defaults to `http://127.0.0.1:8080/v1`, and set `LLM_MODEL` if your endpoint uses a different model name from `local-model`. Use a trusted local endpoint for sensitive transcripts.

Rules look for payment requests, sensitive information, urgency, and attempts to prevent verification. The model can flag additional requests for review. Rule flags stand even when the model clears a transcript. If the endpoint fails or returns an unusable response, the result reports the model as unavailable and retains the rule assessment. The tool assesses transcript content for social engineering. Speaker identity and audio provenance require independent evidence.

## Operational controls

For sensitive requests, pause and call back using a number from the trusted directory. Require a second approver for payments and account changes. Limit who can authorize or execute those changes. Apply these controls even when triage finds no signals.
