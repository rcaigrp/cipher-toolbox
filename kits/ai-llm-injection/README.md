# AI LLM Injection Detection

## Threat Overview

An LLM injection attack occurs when an attacker manipulates inputs to a large language model in a way that allows them to influence the model's behavior or extract sensitive information. This can include prompt injection, where malicious input is crafted to override intended instructions.

This vulnerability was demonstrated in ZDI-26-1121 affecting LM Studio's MCP tool schema processing, where inadequate validation allowed attackers to inject code that would be executed in the service account context.

## Real Examples

The ZDI-26-1121 advisory describes a specific case where LM Studio's processing of MCP tool schemas lacked proper validation. Attackers could supply malicious schemas that would be used to generate code, leading to remote code execution.

## Exposure

Systems using LLMs or AI agents that process user inputs without proper sanitization are exposed, particularly:
- AI-powered chatbots and assistants
- Code generation tools
- API endpoints accepting user prompts
- Systems processing external tool descriptions or schemas

## Countermeasure Approach

The solution provides a detection mechanism for potential LLM injection attempts by analyzing input patterns and applying both rule-based and AI-assisted detection methods.

### Features:
- **AI Detection**: Uses an LLM endpoint (default: `http://127.0.0.1:8080/v1`) to analyze prompts
- **Rule-Based Fallback**: Operates without AI when the model is unavailable
- **Sample Test Cases**: Includes benign and malicious test cases for validation

### How It Works:
1. Analyze input prompt using both AI model and predefined rules
2. Score the prompt based on detected risk factors related to injection attempts
3. Flag if the prompt exceeds a threshold indicating potential injection attempt
4. Log all flagged inputs for review by security team

## Running the Countermeasure

To use this countermeasure:

1. Set up an OpenAI-compatible LLM endpoint at `http://127.0.0.1:8080/v1`
2. Run the test script:
   ```bash
   python3 check_injection.py --test
   ```

For production use:
```bash
python3 check_injection.py --input "Your prompt here"
```

## Non-AI Controls

- Implement strict input validation for all user-supplied data
- Use sandboxing techniques when processing external schemas or inputs
- Maintain allow-lists of trusted tool descriptions and schemas
- Monitor logs for anomalous behavior patterns