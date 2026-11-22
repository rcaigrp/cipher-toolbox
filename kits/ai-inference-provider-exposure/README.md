# Inference provider prompt exposure

Third-party inference endpoints process prompts in cleartext during inference. A compromised provider or an unexpected routing decision can expose customer data. OpenRouter reported removing three providers and removing 125 endpoints from zero-data-retention eligibility after investigating reports of compromised data or failures to uphold data policies. Dragos used synthetic canary tokens to investigate where submitted prompt data surfaced. [OpenRouter incident announcement](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/) · [Dragos research](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens)

Teams routing internal documents, support transcripts, source code, or tool output through third-party endpoints should check the actual routed destination before sending data. The same exposure can arise through automatic fallback routes and tools that forward model inputs to other processors.

## Run the local preflight check

```sh
python3 detect_exposure.py --rules-only --approved-destination --classification public --retention zero-retention-asserted < samples/benign.txt
python3 detect_exposure.py --rules-only --approved-destination --classification public --retention zero-retention-asserted < samples/sensitive-looking.txt
```

The standard-library CLI reads a prompt from stdin and returns JSON. Exit code `1` means review is required. Exit code `0` means the check found no signal. Set `--approved-destination` only after verifying the actual routed endpoint against your allow-list. Unknown classification and retention settings require review.

Without `--rules-only`, the checker sends classification, destination approval, asserted retention, and indicator names to an OpenAI-compatible loopback endpoint. Configure it with `LLM_URL` (default `http://127.0.0.1:8080/v1`) and `LLM_MODEL` (default `local-reviewer`). The request omits raw prompt text and matched values. A model can add a review signal. If the model is unavailable, the local rules still apply.

This is a preflight risk check. Its inputs include caller-supplied assertions, and its output cannot establish whether a provider retained, leaked, or stole prompts.

## Prepare now

Allow-list actual inference endpoints and fallback routes, keep restricted data on approved infrastructure, and require human approval for routing exceptions. Limit agent access to secrets and review recent routing records against provider incident notices and contractual retention terms.
