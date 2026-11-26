# AI Jailbreak Detection Kit

## Threat Overview

An LLM jailbreak occurs when an attacker bypasses safety measures in a large language model (LLM) to force it into generating harmful, inappropriate, or unauthorized content. This can be done through prompt injection, indirect prompt injection, or other techniques that manipulate the model's behavior.

## Real Examples

- Researchers have demonstrated how attackers can use specific prompt structures to bypass content filters in models like ChatGPT.
- In one case, a malicious user was able to extract sensitive information from an LLM by carefully crafting prompts that exploited vulnerabilities in the model's safety protocols.

## Who Is Exposed?

Organizations using LLMs in their applications, especially those with untrusted input or exposed APIs, are at risk. This includes:
- Chatbots and virtual assistants
- Code generation tools
- Content moderation systems
- Agent-based workflows

## How the Countermeasure Works

This kit provides an AI-powered detection system that uses a language model to assess whether a prompt is potentially malicious or attempting a jailbreak. It also includes rule-based checks as a fallback when no AI model is available.

The detection works by:
1. Analyzing input prompts for known patterns of jailbreak attempts
2. Using an LLM to evaluate the intent and structure of the prompt
3. Returning a confidence score indicating likelihood of malicious intent

## Running the Kit

Run the test script with `python3 test.py`.
