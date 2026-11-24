# AI Data Poisoning Detection Kit

## Threat Overview

**Data poisoning** is an integrity attack that manipulates training data to compromise the performance, security, or ethical behavior of large language models (LLMs). This can introduce backdoors, biases, or vulnerabilities into the model, leading to harmful outputs.

### Real Examples:
- In 2025, researchers demonstrated how attackers could poison datasets used for fine-tuning models to cause them to generate false information.
- The "PoisonGPT" attack involved hiding a lobotomized LLM on Hugging Face that spread fake news when activated.
- A backdoor was implanted in an open-source model through malicious pickling, which allowed remote code execution upon loading.

### Who Is Exposed?
Organizations using LLMs in production environments—especially those relying on external or shared datasets—are vulnerable to data poisoning. If training data isn't vetted properly, even a small amount of poisoned content can corrupt the entire model.

### How the Countermeasure Works
This kit provides a detection script that:
1. Analyzes input prompts for signs of known poisoning techniques.
2. Uses an AI model (via `LLM_URL`) to assess prompt integrity.
3. Flags suspicious inputs based on thresholds and model confidence.
4. Falls back to rule-based checks when no AI model is available.

### How to Run
```bash
python detect_poisoning.py --input "prompt text here"
```

Test with sample benign and malicious prompts included in this kit.

## Non-AI Controls
- Implement strict data vetting protocols for all training data sources.
- Use data version control (DVC) to track changes and detect manipulation.
- Employ sandboxing to isolate model interactions with untrusted data.
- Regularly audit datasets for anomalies using anomaly detection tools.