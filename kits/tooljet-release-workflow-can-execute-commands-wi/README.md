# ToolJet Release Workflow Command Injection (CVE-2026-137964)

## Overview
This defensive kit addresses CVE-2026-137964, a critical command injection vulnerability in ToolJet's GitHub Actions release workflow. The flaw allows attackers to execute arbitrary commands with cross-repository permissions via malicious pull request titles.

## Who is Exposed
Organizations using ToolJet versions <= 3.21.61-beta that have GitHub Actions workflows configured for releases are exposed. This includes any system that uses ToolJet's release automation with a GITHUB_TOKEN.

## Files in this Kit
- `check_exposure.py`: Checks if the local system is running an affected ToolJet version
- `mitigate.py`: Implements vendor-recommended hardening (dry-run by default)
- `hunt.md`: Hunting queries for detecting exploitation attempts