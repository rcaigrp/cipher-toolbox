# Model artifact intake triage

Treat third-party checkpoints as software. A loader that deserializes an untrusted checkpoint can execute code with the privileges of the loading process. Model downloaders, conversion jobs, CI pipelines, and serving workers are exposed when they load artifacts automatically. The same class applies to adapters, cached checkpoints, and bundled custom loaders.

JFrog documented a malicious model published on Hugging Face in 2024 and described follow-up repository scanning with Hugging Face in 2025. The reports establish that malicious artifacts were published. The extent of downstream compromise is unknown from the available material. OWASP covers third-party models and related components under LLM03 Supply Chain.

- [JFrog malicious model investigation](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [JFrog and Hugging Face follow-up](https://jfrog.com/blog/jfrog-and-hugging-face-join-forces/)
- [OWASP LLM03 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
- [Hugging Face model safety guidance](https://huggingface.co/docs/text-generation-inference/main/basic_tutorials/safety)

## Run locally

Requires Python 3. Use `python3 scanner.py /path/to/artifact` or add `--rules-only` to skip the endpoint. Run the tests with `python3 -m unittest -v`. The tests generate temporary inert fixtures and mock endpoint responses.

The scanner reads a local file without loading or extracting it. It computes SHA-256 and flags selected extensions and header signatures. It sends only normalized format signals and rule findings to the OpenAI-compatible `/chat/completions` endpoint. Set `LLM_URL` to override the default `http://127.0.0.1:8080/v1` and `LLM_MODEL` to override `local-model`. A model can add a review flag. Rule findings remain in force if the model is unavailable or gives an invalid response.

Exit 0 means no signal from these limited checks. Exit 1 means review and exit 2 means the input could not be inspected. The scanner does not validate safetensors structure, inspect archive contents, verify provenance, or detect poisoned weights. A hash provides an integrity check only when compared against a trusted expected digest.

## Prepare before disclosure

Inventory every job that fetches, converts, or loads artifacts. Allow-list publishers and formats, pin immutable revisions, and verify signed provenance or trusted digests before promotion. Prefer safetensors through a vetted loader and disable repository-provided code. Require human approval for format or loader exceptions. Keep conversion workers isolated with least privilege, no credentials, and restricted egress.
