# Hunting for ToolJet Command Injection Exploitation (CVE-2026-137964)

## Overview
This document contains hunting queries to detect potential exploitation of CVE-2026-137964, a command injection vulnerability in ToolJet's GitHub Actions release workflow.

## Detection Logic
The vulnerability manifests when:
1. A pull request with shell metacharacters in the title is merged
2. The PR title is used directly in a GitHub Actions workflow without sanitization
3. This triggers execution of commands with elevated permissions

## Hunting Queries

### GitHub Audit Logs (if available)
```bash
# Search for workflows triggered by pull request merges with suspicious titles
# This would be run against GitHub audit logs or similar system
```

### Git Log Analysis
```bash
# Check recent commits for patterns that might indicate exploitation
git log --oneline --grep=";" --since="2026-11-01"
git log --oneline --grep="&" --since="2026-11-01"
git log --oneline --grep="|" --since="2026-11-01"
git log --oneline --grep="`" --since="2026-11-01"
```

### Workflow Event Logs (if available)
```bash
# If you have access to GitHub Actions event logs:
# Look for workflow runs where the PR title contained shell metacharacters
# This would be done by analyzing the events in your logging system
```

## Indicators of Compromise (IOCs)
- Pull request titles containing shell metacharacters: `;`, `&`, `|`, `` ` ``
- Workflow runs with unusual command execution patterns
- Unusual network connections from GitHub Actions runners

## Remediation Steps
1. Update to ToolJet 3.21.96-LTS or later
2. Review and sanitize all GitHub Actions workflows that use PR titles in shell contexts
3. Implement proper input validation for all user-provided data
4. Monitor for suspicious workflow activity