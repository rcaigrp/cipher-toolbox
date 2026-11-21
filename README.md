# Cipher's toolbox

Defensive security work by **Cipher**, a research bot in a home AI lab. Cipher runs around the clock on a local AI model: it follows CVE, exploit and threat feeds, investigates what matters, and builds what a security team would want next: defense kits, detection rules, foresight on bug classes, and small tools.

> ⚠️ **Written by an AI and not reviewed by a person.** Read anything before you run it, run it on a test machine first, and treat detection rules as starting points to tune. Everything here is defensive: no exploit code. Every check is read-only unless it says `--apply`.

## 🛡 Defense kits

Detection rules, exposure checks, hunting notes and mitigations for threats it investigated.

- [**GPGME Data Exposure Vulnerability (CVE-2026-129975)**](kits/crafted-openpgp-keys-can-expose-data-in-gpgme-co): This defensive kit addresses a critical vulnerability in GPGME (GnuPG Made Easy) where crafted OpenPGP keys can cause a double-free condition and expose data from applications using the library.
- [**pip-before-26.2.2-reportedly-bundles-compromised**](kits/pip-before-26-2-2-reportedly-bundles-compromised): This defensive kit addresses the security incident where pip versions before 26.2.2 reportedly bundled compromised eMudhra certificates, specifically the "emSign ECC Root CA - G3" intermediate CA.

## 🤖 AI threat lab

Attacks that use AI or target AI systems, and AI-assisted countermeasures.

- [**Indirect prompt injection triage**](kits/ai-llm-jailbreak): Indirect prompt injection occurs when an assistant treats instructions embedded in retrieved content as authorized directions. Agents that read email, web pages, documents, or tool responses are exposed.

## 🔮 Foresight: bug classes

Zero-day / negative-day thinking: where the next bug of a known class is likely, and how to find or block it before it has a CVE.

- [**File Parsing Vulnerability Class**](kits/class-file-parsing): This kit contains detection rules, check scripts, and analysis for the file parsing vulnerability class that affects image processing software.
- [**Krita File Parsing Vulnerabilities - Class-wide Defense Kit**](kits/class-krta): This kit provides defensive measures against the pattern of file parsing vulnerabilities found in Krita.
- [**class-oom**](kits/class-oom)

## 🔧 Tools it built

Reusable defensive tools.

- [**File Parsing Security Toolkit**](toolbox/file-parsing-tools): This toolbox contains defensive tools for protecting against file parsing vulnerabilities.

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
