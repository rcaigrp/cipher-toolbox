# AI Inference Data Exposure Detector

## Threat Overview

This kit detects potential data exposure in AI inference services by analyzing prompts for signs of data leakage or unauthorized access attempts. It's designed to identify when sensitive information might be inadvertently exposed through AI interactions.

### Real Examples

- OpenRouter incident where prompt theft was discovered through canary tokens
- Dragos research showing widespread failures in data retention policies among AI providers
- AI supply chain breaches where customer data was compromised

### Who Is Exposed?

- Organizations using AI inference services (OpenAI, Anthropic, Google, etc.)
- Developers integrating AI into applications or workflows
- Companies that handle sensitive data and use AI-powered tools

## Countermeasure Approach

This solution:
1. **Analyzes prompts** for potential data leakage patterns
2. **Identifies suspicious content** that might expose sensitive information
3. **Provides risk assessment** based on rule-based detection and optional LLM analysis

## How It Works

The system evaluates prompts using:
- Static rules to detect known patterns of sensitive data exposure
- Optional machine learning model for advanced pattern recognition
- Risk scoring to categorize potential exposures

## Usage

```bash
python data_exposure_detector.py --prompt "your prompt here"
```

## Testing

Run tests with:
```bash
python test_data_exposure_detector.py
```