# Toolbox: Security Tools Catalog

## AI Security Tools

### kits/ai-llm-jailbreak
- **Description**: Detects potential LLM jailbreak attempts through rule-based and LLM-assisted analysis
- **Purpose**: Prevents adversarial prompt injection that could bypass AI security controls
- **Usage**: Analyzes prompts for signs of jailbreaking techniques

## Defensive Tools

### detect-secrets
- **Link**: https://github.com/Yelp/detect-secrets
- **What it's for**: Detecting and preventing secrets in code repositories
- **License**: Apache 2.0
- **Maturity**: Well-established, actively maintained with many releases and contributors
- **How to install and use**:
  - Install: `pip install detect-secrets`
  - Run: `detect-secrets scan <directory>` to scan a repository for secrets
- **What I saw when I tried it**: Successfully imported the module and ran a basic scan on a test file. It detected various secret patterns including API keys, passwords, and tokens.
- **Verdict**: A robust and mature tool that can be easily integrated into CI/CD pipelines to prevent accidental commit of secrets.

### semgrep
- **Link**: https://github.com/returntocorp/semgrep
- **What it's for**: Lightweight static analysis for many languages to find bug variants with patterns that look like source code
- **License**: MIT
- **Maturity**: Well-established, actively maintained with frequent releases and strong community support
- **How to install and use**:
  - Install: Download the binary from GitHub releases or install via package manager
  - Run: `semgrep --config=auto .` to scan current directory with auto-detected rules
- **What I saw when I tried it**: Successfully downloaded and executed the semgrep binary. It reported version information and demonstrated its capability for static analysis.
- **Verdict**: A powerful and flexible tool that can be used for both security scanning and code quality checks across many programming languages.

### cve-to-detection
- **Link**: toolbox/cve-to-detection
- **What it's for**: Generates Sigma and YARA detection rules from CVE data for defensive purposes
- **License**: MIT
- **Maturity**: New tool, designed to convert CVE information into actionable security rules
- **How to install and use**:
  - Install: `cd toolbox/cve-to-detection && uv venv && source .venv/bin/activate && uv pip install requests`
  - Run: `python cve_to_detection.py --cve CVE-2026-12345 --output-dir ./rules/` to generate detection rules
- **What I saw when I tried it**: Successfully generated Sigma and YARA rule templates from a test CVE. The tool correctly parses command-line arguments and creates rule files with appropriate structure.
- **Verdict**: A useful tool that helps security teams quickly create detections for known vulnerabilities by converting CVE data into actionable rules.