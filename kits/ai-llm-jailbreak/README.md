# AI LLM Jailbreak Defense

## Threat Overview

An LLM jailbreak is an input designed to bypass a large language model's safety training, causing it to produce content it would normally refuse. This can result in unauthorized access to restricted information, generation of harmful content, or violation of usage policies.

### Key Examples:
- **Persona Hijacking**: Prompting the model to assume a different identity or role
- **Multi-turn Escalation**: Using conversation history to gradually push the model into unsafe territory
- **Payload Splitting**: Breaking malicious prompts into smaller parts that evade detection

## Who Is Exposed?
Organizations using LLMs in applications, chatbots, or agents are at risk if they don't implement proper input sanitization and safety measures.

## How the Countermeasure Works
This defense uses an AI-based scanner to detect potential jailbreak attempts in user inputs. It includes:
- A machine learning model for detecting jailbreak patterns (defaulting to a local endpoint)
- A rule-based fallback for when no AI model is available
- Test cases and validation

## Running the Countermeasure
Run the script with `python3 scanner.py`. The default LLM endpoint is set to `http://127.0.0.1:8080/v1`.