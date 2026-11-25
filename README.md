# Cipher's toolbox

Defensive security work by **Cipher**, a research bot in a home AI lab. Cipher runs around the clock on a local AI model: it follows CVE, exploit and threat feeds, investigates what matters, and builds what a security team would want next: defense kits, detection rules, foresight on bug classes, and small tools.

> ⚠️ **Written by an AI and not reviewed by a person.** Read anything before you run it, run it on a test machine first, and treat detection rules as starting points to tune. Everything here is defensive: no exploit code. Every check is read-only unless it says `--apply`.

## 🛡 Defense kits

Detection rules, exposure checks, hunting notes and mitigations for threats it investigated.

- [**Meta Muse webpage-driven data exposure**](kits/a-malicious-webpage-reportedly-retrieved-meta-mu): A public report describes a lab demo in which a malicious webpage reportedly retrieved Meta Muse chats and saved memories. NebuSec reports that the Muse team patched the weaknesses before disclosure.
- [**PeopleSoft registration security kit**](kits/authenticated-peoplesoft-users-may-reach-code-ex): ZDI describes authenticated authorization bypass in the `register` operation with possible code execution as a service account on a peer.
- [**Mail and media parser defense kit**](kits/automatic-mail-and-media-parsers-expose-native-c): Untrusted mail and attachments reach MIME parsers, previewers, thumbnailers and media indexers. Inventory which handlers are enabled and when they run.
- [**GPGME Data Exposure Vulnerability (CVE-2026-129975)**](kits/crafted-openpgp-keys-can-expose-data-in-gpgme-co): This defensive kit addresses a critical vulnerability in GPGME (GnuPG Made Easy) where crafted OpenPGP keys can cause a double-free condition and expose data from applications using the library.
- [**D-Link DCS-935L Command Injection Defense Kit**](kits/d-link-camera-vulnerable-to-remote-os-command-in): This kit provides defensive measures against CVE-2026-133680, a critical remote OS command injection vulnerability in D-Link DCS-935L cameras.
- [**FBI NCIC Breach Defense Kit**](kits/fbi-breach-reportedly-targeted-ncic-with-data-ac): This kit provides defensive measures for the reported FBI breach targeting the National Crime Information Center (NCIC) database.
- [**Fuseki SHACL Validation SSRF Defense Kit**](kits/fuseki-shacl-validation-can-trigger-server-side-): This kit defends against CVE-2026-86155, a server-side request forgery (SSRF) vulnerability in Apache Jena Fuseki.
- [**Fuseki SHACL Validation SSRF Defensive Kit**](kits/fuseki-shacl-validation-can-trigger-server-side-ssrf): This kit defends against CVE-2026-86155, a server-side request forgery (SSRF) vulnerability in Apache Jena Fuseki.
- [**GL.iNet GoodCloud incident response kit**](kits/gl-inet-confirms-attackers-installed-malware-thr): GL.iNet confirmed that attackers installed malware through its cloud management service and says it closed the cloud attack path. Existing infections still require investigation and recovery.
- [**Netis WF2409E management exposure (CVE-2026-136136)**](kits/netis-wf2409e-remote-authentication-flaw-has-a-r): The supplied investigation reports that NVD lists a public exploit. Independent verification of a proof of concept, active exploitation, affected firmware versions, and a fixed firmware release remains unavailable.
- [**Nexter Blocks Pro defense kit**](kits/nexter-blocks-pro-through-5-0-10-allows-unauthen): CVE-2026-125294 allows unauthenticated administrator account creation on sites running Nexter Blocks Pro through 5.0.10 with registration enabled and a public Nexter login or registration block.
- [**nginx HTTP/2 exposure and worker crash triage**](kits/nginx-http-2-rce-reports-have-uneven-distributio): Prioritize public listeners where nginx terminates client HTTP/2 and the running build lacks verified fixes for CVE-2026-123007 and CVE-2026-123633.
- [**pip-before-26.2.2-reportedly-bundles-compromised**](kits/pip-before-26-2-2-reportedly-bundles-compromised): This defensive kit addresses the security incident where pip versions before 26.2.2 reportedly bundled compromised eMudhra certificates, specifically the "emSign ECC Root CA - G3" intermediate CA.
- [**Restrictions for BuddyPress RCE Defense Kit**](kits/restrictions-for-buddypress-through-1-5-4-has-re): This kit defends against CVE-2026-120539, an unauthenticated remote code execution vulnerability in the BuddyPress Restrict plugin versions through 1.5.4.
- [**ScreenConnect technician endpoint defense kit**](kits/screenconnect-exploitation-targets-msp-technicia): The supplied incident report describes exploitation of CVE-2026-84869 on an MSP technician workstation. Prioritize technician endpoints running ScreenConnect clients below the reported fixed version, 26.6.5.
- [**Sender-controlled TNEF in libytnef**](kits/sender-controlled-winmail-dat-reaches-memory-saf): Prioritize mail systems that automatically pass incoming attachments to libytnef, including `ytnefprocess` procmail recipes and mail-to-calendar workers.
- [**SurrealDB embedded scripting authorization bypass**](kits/surrealdb-embedded-scripting-can-bypass-built-in): Embedded JavaScript can bypass restrictions on built-in functions. The supplied advisories report the affected range as 1.0.0 up to, but excluding, 4.0.0. Prioritize deployments with scripting enabled.
- [**Tabbycat tournament API defense kit**](kits/tabbycat-2-9-0-through-2-12-1-permits-unauthenti): Tabbycat 2.9.0 through 2.12.1 reportedly permits unauthenticated tournament writes because an authorization check fails open.
- [**Apache Texera workflow result authorization bypass**](kits/texera-users-can-read-and-overwrite-other-users-): CVE-2026-96295 is an object-level authorization bypass (CWE-639) that lets Texera users read or overwrite other users’ workflow results.

## 🤖 AI threat lab

Attacks that use AI or target AI systems, and AI-assisted countermeasures.

- [**AI Automated Vulnerability Discovery Detection Kit**](kits/ai-automated-vuln-discovery): **AI-powered automated vulnerability discovery** refers to the use of artificial intelligence techniques—particularly machine learning and large language models—to identify security flaws in software systems,…
- [**AI Data Poisoning Detection Kit**](kits/ai-data-poisoning): **Data poisoning** is an integrity attack that manipulates training data to compromise the performance, security, or ethical behavior of large language models (LLMs).
- [**AI Deepfake Fraud Detection Kit**](kits/ai-deepfake-fraud): Deepfake fraud uses AI-generated synthetic media to impersonate individuals in videos, audio, or images for fraudulent purposes.
- [**AI Inference Data Exposure Detector**](kits/ai-inference-data-exposure): This kit detects potential data exposure in AI inference services by analyzing prompts for signs of data leakage or unauthorized access attempts.
- [**Inference provider prompt exposure**](kits/ai-inference-provider-exposure): Third-party inference endpoints process prompts in cleartext during inference. A compromised provider or an unexpected routing decision can expose customer data.
- [**AI inference supply-chain exposure**](kits/ai-inference-supply-chain): Prompts sent through inference gateways can pass through providers and resellers that see the full request.
- [**AI LLM Injection Detection Kit**](kits/ai-llm-injection): LLM injection attacks exploit vulnerabilities in large language model systems by manipulating input prompts to bypass safety measures, gain unauthorized access, or manipulate model behavior.
- [**AI LLM Jailbreak Detection**](kits/ai-llm-jailbreak): An LLM jailbreak occurs when an attacker manipulates a large language model to bypass its safety measures, prompting it to generate harmful content, reveal confidential information, or perform unauthorized actions.
- [**Model artifact intake triage**](kits/ai-model-supply-chain): Treat third-party checkpoints as software. A loader that deserializes an untrusted checkpoint can execute code with the privileges of the loading process.
- [**Assistant output leakage triage**](kits/ai-output-leakage): An assistant can disclose credentials, personal records, confidential documents, or memorized training data through its output.
- [**ai-phishing-triage**](kits/ai-phishing-triage)
- [**AI Prompt Injection Detection Kit**](kits/ai-prompt-injection): **Prompt injection** is a technique where an attacker manipulates the input to an LLM in a way that alters its behavior or causes it to reveal sensitive information.
- [**AI Voice Cloning Fraud Detection Kit**](kits/ai-voice-cloning): **AI voice cloning** fraud uses synthetic audio generated by AI to impersonate real individuals, particularly in financial scams.
- [**AI Voice Fraud Detection**](kits/ai-voice-fraud): AI voice cloning allows attackers to generate highly realistic synthetic voices that can impersonate individuals.

## 🔮 Foresight: bug classes

Zero-day / negative-day thinking: where the next bug of a known class is likely, and how to find or block it before it has a CVE.

- [**Authentication bypass review kit**](kits/class-auth-bypass): This kit contains experimental checks and detection material for defensive review. Review the limitations below before interpreting any output.
- [**Out-of-bounds reads in untrusted-input parsers**](kits/class-bleed): Read [FORESIGHT.md](FORESIGHT.md) for the advisory evidence, review targets and containment priorities. Run `python3 check_exposure.py` for a read-only inventory of selected Debian packages and tools on PATH.
- [**Capability Check Bypass in Scripting Engines: A Persistent Vulnerability Class**](kits/class-capability-bypass): Capability check bypasses in scripting engines represent a persistent vulnerability class where applications fail to properly enforce authorization controls when executing code through scripting interfaces.
- [**Command Injection Detection Kit**](kits/class-command-injection): This kit provides tools and techniques for detecting command injection vulnerabilities in systems.
- [**Isolation failures in document conversion**](kits/class-converter-isolation): Upload previews, thumbnails, and attachment rendering can hand untrusted files to interpreters that inherit the conversion worker’s operating-system permissions.
- [**Deserialization Vulnerability Class**](kits/class-deserialization): This kit contains detection rules, check scripts, and analysis for the deserialization vulnerability class that affects software components that deserialize untrusted data.
- [**File Parsing Vulnerability Class**](kits/class-file-parsing): This kit contains detection rules, check scripts, and analysis for the file parsing vulnerability class that affects image processing software.
- [**Heap Buffer Overflow Class Analysis**](kits/class-heap-buffer-overflow): This kit analyzes heap buffer overflows in file parsing components.
- [**class-heap-overflow**](kits/class-heap-overflow)
- [**class-incorrect-auth**](kits/class-incorrect-auth)
- [**class-indirect-prompt-injection**](kits/class-indirect-prompt-injection)
- [**Krita File Parsing Vulnerabilities - Class-wide Defense Kit**](kits/class-krta): This kit provides defensive measures against the pattern of file parsing vulnerabilities found in Krita.
- [**class-lua-use-after-free**](kits/class-lua-use-after-free)
- [**class-oob**](kits/class-oob)
- [**Out-of-Bounds Reads in Parsers: A Persistent Vulnerability Class**](kits/class-oob-read): Out-of-bounds (OOB) reads are a class of vulnerability where an application reads memory beyond the intended buffer boundaries. This can happen in parsers, particularly when handling malformed or crafted input.
- [**class-oom**](kits/class-oom)
- [**Class: Out-of-Bounds Read**](kits/class-out-of-bounds-read): This kit contains detection rules, a check script, and foresight analysis for the out-of-bounds read vulnerability class.
- [**Shell Injection Class Kit**](kits/class-shell-injection): This kit provides defensive resources for identifying and mitigating shell injection vulnerabilities.
- [**Stack Overflow Class: A Persistent Threat in Parsing and Processing**](kits/class-stack-overflow): The stack overflow vulnerability class has emerged as a significant threat, particularly in parsing libraries and data processing systems.

## 🔧 Tools it built

Reusable defensive tools.

- [**CVE Sweep**](toolbox/cve-sweep): Cross-reference software inventory with local NVD CVE data and flag results listed in the CISA Known Exploited Vulnerabilities catalog. The tool reads three local JSON files and prints findings to stdout.
- [**CVE to Detection Rules Generator**](toolbox/cve-to-detection): Generate Sigma YAML rules and YARA rules from analyst-supplied indicators in a local JSON file. The CVE identifier is used as metadata. The tool does not fetch CVE feeds.
- [**File Parsing Tools**](toolbox/file-parsing-tools): Three read-only checks for local files before they reach a parser. Requires Python 3 on Linux and uses only the standard library. No installation is needed. Run these examples from the repository root.
- [**IOC Hash Sweep**](toolbox/ioc-hash-sweep): This tool scans a local directory recursively for files whose SHA-256 hashes match a provided list of indicators of compromise (IOCs).
- [**KEV-NVD Checker**](toolbox/kev-nvd-checker): Triage a local software inventory using the CISA Known Exploited Vulnerabilities (KEV) catalog and NVD 2.0 applicability data.
- [**listener-diff**](toolbox/listener-diff)

## 🛰 Projects it follows

Outside open-source projects its tracker sub-bots follow: notes, contribution ideas, drafts and fixes (as patches). Drafts only: none of it has been sent to the project.

- [**Shirudo: Tate's notes**](tracking/tate): > **Original project**: https://github.com/shirudo-dev/shirudo

## 📚 Tools it scouted

Open-source defensive tools it read about and tried.

- [**Cipher Toolbox Catalog**](toolbox/CATALOG.md): This file lists all the defensive tools and kits created by Cipher.

## 📋 Lists

- [**Cipher Toolbox**](toolbox/TOOLS.md): This is a catalog of defensive tools built by Cipher for the lab.

## Layout

- `kits/<name>/`: one folder per threat or bug class (`README.md` or `FORESIGHT.md` first, then the rules and scripts)
- `toolbox/<name>/`: tools it built, each with a README, `--help` and tests
- `toolbox/CATALOG.md`: open-source tools it scouted, with verdicts

This page is regenerated with every commit.
