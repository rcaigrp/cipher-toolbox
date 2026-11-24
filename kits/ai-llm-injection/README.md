# AI Indirect Prompt Injection Detection Kit

## Threat Overview

**Indirect prompt injection** occurs when an attacker manipulates inputs that are processed by an LLM but not directly part of the prompt. These attacks exploit vulnerabilities in how data flows through systems, particularly in agent-based or multi-step workflows where external data sources can be manipulated.

### Real Examples:
- In 2026, attackers used indirect injection to manipulate a chatbot's knowledge base by submitting malicious documents that were indexed and later referenced during conversations.
- A vulnerability was found in an AI assistant that accepted user-submitted URLs as input. By crafting a URL pointing to a malicious page, attackers could inject data into the LLM's context indirectly.
- In another case, an automated agent used external APIs for context but did not validate inputs properly. An attacker manipulated the API response to inject malicious instructions.

### Who Is Exposed?
Organizations using AI agents or chatbots that interact with external data sources (e.g., websites, databases, file uploads) are vulnerable if they do not properly sanitize or validate all input before it reaches the LLM. Any system where LLM behavior depends on external context without proper validation is at risk.

### How the Countermeasure Works
This kit provides a detection script that:
1. Analyzes inputs for known indirect injection patterns.
2. Uses an AI model (via `LLM_URL`) to score potential indirect injection attempts.
3. Flags suspicious inputs based on thresholds and model confidence.
4. Falls back to rule-based checks when no AI model is available.

### How to Run
```bash
python detect_indirect_injection.py --input "user input here"
```

Test with sample benign and malicious prompts included in this kit.

## Non-AI Controls
- Implement strict input validation for all external data sources.
- Sanitize and escape inputs before passing them to the LLM.
- Use allowlists for trusted domains or file types.
- Employ network segmentation and access controls to limit exposure.