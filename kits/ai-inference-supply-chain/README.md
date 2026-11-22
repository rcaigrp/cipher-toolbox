# AI inference supply-chain exposure

Prompts sent through inference gateways can pass through providers and resellers that see the full request. Teams that send customer data, internal documents, or operational details to hosted inference are exposed when the actual processing route is opaque or a provider is compromised.

Dragos reported canary activity consistent with at least three provider compromises, prompt access through reseller logging, and delayed access to canary URLs in requests marked Zero Data Retention. A canary signals exposure but does not by itself identify the responsible hop. [Dragos research](https://www.dragos.com/blog/ai-supply-chain-security-canary-tokens)

OpenRouter said it removed three providers and took 125 endpoints off its Zero Data Retention eligibility list. It attributed the findings to inference providers and said its own platform showed no evidence of unauthorized access. [OpenRouter incident notice](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/)

## Countermeasure

Run the preflight before dispatching a prompt to hosted inference. Rules flag recognizable sensitive material and check the declared provider against an explicit allow-list. An optional local LLM adds a semantic check for sensitive context that lacks obvious markers. Rule findings take precedence. The preflight does not dispatch the prompt or verify the provider's actual routing or retention practices.

## Run

From this directory, run `python3 preflight.py --provider approved-example --allow-provider approved-example --rules-only < samples/benign.txt`. Remove `--rules-only` to enable semantic review. Set `LLM_URL` to a loopback OpenAI-compatible API base if needed. The default is `http://127.0.0.1:8080/v1`. Set `LLM_MODEL` to the identifier served by your endpoint. If the model is unavailable or returns an invalid verdict, the result reports rules-only coverage. Run `python3 -m unittest -v` to exercise the local tests.

## Controls to prepare now

Require explicit provider and route approval at the inference gateway, disable automatic routing to unapproved providers, keep restricted data on approved local infrastructure, and require human review before making exceptions. Collect provider and route metadata without logging prompt bodies. Give classifiers no tools or credentials and restrict their network access to the local model endpoint. Review recent inference routes and prioritize any requests that carried secrets or regulated data.