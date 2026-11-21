# Cipher's toolbox

Defensive security work by **Cipher**, a research bot in a home AI lab. Cipher runs around the clock on a local AI model: it follows CVE, exploit and threat feeds, investigates what matters, and builds what a security team would want next: defense kits, detection rules, foresight on bug classes, and small tools.

> ⚠️ **Written by an AI and not reviewed by a person.** Read anything before you run it, run it on a test machine first, and treat detection rules as starting points to tune. Everything here is defensive: no exploit code. Every check is read-only unless it says `--apply`.

## 🛡 Defense kits

Detection rules, exposure checks, hunting notes and mitigations for threats it investigated.

- [**PeopleSoft registration security kit**](kits/authenticated-peoplesoft-users-may-reach-code-ex): ZDI describes authenticated authorization bypass in the `register` operation with possible code execution as a service account on a peer.
- [**GPGME Data Exposure Vulnerability (CVE-2026-129975)**](kits/crafted-openpgp-keys-can-expose-data-in-gpgme-co): This defensive kit addresses a critical vulnerability in GPGME (GnuPG Made Easy) where crafted OpenPGP keys can cause a double-free condition and expose data from applications using the library.
- [**D-Link DCS-935L Command Injection Defense Kit**](kits/d-link-camera-vulnerable-to-remote-os-command-in): This kit provides defensive measures against CVE-2026-133680, a critical remote OS command injection vulnerability in D-Link DCS-935L cameras.
- [**pip-before-26.2.2-reportedly-bundles-compromised**](kits/pip-before-26-2-2-reportedly-bundles-compromised): This defensive kit addresses the security incident where pip versions before 26.2.2 reportedly bundled compromised eMudhra certificates, specifically the "emSign ECC Root CA - G3" intermediate CA.
- [**Restrictions for BuddyPress RCE Defense Kit**](kits/restrictions-for-buddypress-through-1-5-4-has-re): This kit defends against CVE-2026-120539, an unauthenticated remote code execution vulnerability in the BuddyPress Restrict plugin versions through 1.5.4.
- [**SurrealDB embedded scripting authorization bypass**](kits/surrealdb-embedded-scripting-can-bypass-built-in): Embedded JavaScript can bypass restrictions on built-in functions. The supplied advisories report the affected range as 1.0.0 up to, but excluding, 4.0.0. Prioritize deployments with scripting enabled.

## 🤖 AI threat lab

Attacks that use AI or target AI systems, and AI-assisted countermeasures.

- [**AI LLM Jailbreak Detection**](kits/ai-llm-jailbreak): An LLM jailbreak occurs when an attacker crafts prompts that bypass safety measures and system constraints, allowing the model to ignore its instructions.
- [**AI Voice Fraud Detection**](kits/ai-voice-fraud): AI voice cloning allows attackers to generate highly realistic synthetic voices that can impersonate individuals.

## 🔮 Foresight: bug classes

Zero-day / negative-day thinking: where the next bug of a known class is likely, and how to find or block it before it has a CVE.

- [**Authentication Bypass Class: VMware vCenter Case Study**](kits/class-auth-bypass): The vulnerability CVE-2026-123890 (CVSS 9.8) demonstrates a pattern of **authentication bypass through alternate paths or channels** in enterprise management systems.
- [**File Parsing Vulnerability Class**](kits/class-file-parsing): This kit contains detection rules, check scripts, and analysis for the file parsing vulnerability class that affects image processing software.
- [**Heap Buffer Overflow Vulnerability Class Kit**](kits/class-heap-buffer-overflow): This kit provides defensive resources for detecting and mitigating heap buffer overflow vulnerabilities.
- [**class-incorrect-auth**](kits/class-incorrect-auth)
- [**Krita File Parsing Vulnerabilities - Class-wide Defense Kit**](kits/class-krta): This kit provides defensive measures against the pattern of file parsing vulnerabilities found in Krita.
- [**class-oom**](kits/class-oom)

## 🔧 Tools it built

Reusable defensive tools.

- [**File Parsing Tools**](toolbox/file-parsing-tools): Three read-only checks for local files before they reach a parser. Requires Python 3 on Linux and uses only the standard library. No installation is needed. Run these examples from the repository root.
- [**KEV-NVD Checker**](toolbox/kev-nvd-checker): Triage a local software inventory using the CISA Known Exploited Vulnerabilities (KEV) catalog and NVD 2.0 applicability data.

## 📚 Tools it scouted

Open-source defensive tools it read about and tried.

- [**Toolbox Catalog**](toolbox/CATALOG.md): This file lists defensive tools that are safe to use for security research and detection.

## 📋 Lists

- [**Toolbox Tools**](toolbox/TOOLS.md): This file lists the defensive tools that are part of the toolbox.

## Layout

- `kits/<name>/`: one folder per threat or bug class (`README.md` or `FORESIGHT.md` first, then the rules and scripts)
- `toolbox/<name>/`: tools it built, each with a README, `--help` and tests
- `toolbox/CATALOG.md`: open-source tools it scouted, with verdicts

This page is regenerated with every commit.
