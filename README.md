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
- [**GL.iNet GoodCloud incident response kit**](kits/gl-inet-confirms-attackers-installed-malware-thr): GL.iNet confirmed that attackers installed malware through its cloud management service and says it closed the cloud attack path. Existing infections still require investigation and recovery.
- [**Nexter Blocks Pro defense kit**](kits/nexter-blocks-pro-through-5-0-10-allows-unauthen): CVE-2026-125294 allows unauthenticated administrator account creation on sites running Nexter Blocks Pro through 5.0.10 with registration enabled and a public Nexter login or registration block.
- [**nginx HTTP/2 exposure and worker crash triage**](kits/nginx-http-2-rce-reports-have-uneven-distributio): Prioritize public listeners where nginx terminates client HTTP/2 and the running build lacks verified fixes for CVE-2026-123007 and CVE-2026-123633.
- [**pip-before-26.2.2-reportedly-bundles-compromised**](kits/pip-before-26-2-2-reportedly-bundles-compromised): This defensive kit addresses the security incident where pip versions before 26.2.2 reportedly bundled compromised eMudhra certificates, specifically the "emSign ECC Root CA - G3" intermediate CA.
- [**Restrictions for BuddyPress RCE Defense Kit**](kits/restrictions-for-buddypress-through-1-5-4-has-re): This kit defends against CVE-2026-120539, an unauthenticated remote code execution vulnerability in the BuddyPress Restrict plugin versions through 1.5.4.
- [**Sender-controlled TNEF in libytnef**](kits/sender-controlled-winmail-dat-reaches-memory-saf): Prioritize mail systems that automatically pass incoming attachments to libytnef, including `ytnefprocess` procmail recipes and mail-to-calendar workers.
- [**SurrealDB embedded scripting authorization bypass**](kits/surrealdb-embedded-scripting-can-bypass-built-in): Embedded JavaScript can bypass restrictions on built-in functions. The supplied advisories report the affected range as 1.0.0 up to, but excluding, 4.0.0. Prioritize deployments with scripting enabled.
- [**Apache Texera workflow result authorization bypass**](kits/texera-users-can-read-and-overwrite-other-users-): CVE-2026-96295 is an object-level authorization bypass (CWE-639) that lets Texera users read or overwrite other users’ workflow results.

## 🤖 AI threat lab

Attacks that use AI or target AI systems, and AI-assisted countermeasures.

- [**AI Deepfake Fraud Detection Kit**](kits/ai-deepfake-fraud): Deepfake fraud uses AI-generated synthetic media to impersonate individuals in videos, audio, or images for fraudulent purposes.
- [**AI Inference Data Exposure Detector**](kits/ai-inference-data-exposure): This kit detects potential data exposure in AI inference services by analyzing prompts for signs of data leakage or unauthorized access attempts.
- [**Inference provider prompt exposure**](kits/ai-inference-provider-exposure): Third-party inference endpoints process prompts in cleartext during inference. A compromised provider or an unexpected routing decision can expose customer data.
- [**AI inference supply-chain exposure**](kits/ai-inference-supply-chain): Prompts sent through inference gateways can pass through providers and resellers that see the full request.
- [**AI LLM Jailbreak Detection**](kits/ai-llm-jailbreak): An **LLM jailbreak** occurs when an attacker manipulates an AI assistant to bypass its safety measures, causing it to reveal confidential information or perform unauthorized actions.
- [**Model artifact intake triage**](kits/ai-model-supply-chain): Treat third-party checkpoints as software. A loader that deserializes an untrusted checkpoint can execute code with the privileges of the loading process.
- [**Assistant output leakage triage**](kits/ai-output-leakage): An assistant can disclose credentials, personal records, confidential documents, or memorized training data through its output.
- [**AI Voice Cloning Fraud Detection Kit**](kits/ai-voice-cloning): **AI voice cloning** fraud uses synthetic audio generated by AI to impersonate real individuals, particularly in financial scams.
- [**AI Voice Fraud Detection**](kits/ai-voice-fraud): AI voice cloning allows attackers to generate highly realistic synthetic voices that can impersonate individuals.

## 🔮 Foresight: bug classes

Zero-day / negative-day thinking: where the next bug of a known class is likely, and how to find or block it before it has a CVE.

- [**Authentication Bypass Class: VMware vCenter Case Study**](kits/class-auth-bypass): The vulnerability CVE-2026-123890 (CVSS 9.8) demonstrates a pattern of **authentication bypass through alternate paths or channels** in enterprise management systems.
- [**Out-of-bounds reads in untrusted-input parsers**](kits/class-bleed): Read [FORESIGHT.md](FORESIGHT.md) for the advisory evidence, review targets and containment priorities. Run `python3 check_exposure.py` for a read-only inventory of selected Debian packages and tools on PATH.
- [**Capability Check Bypass in Scripting Engines: A Persistent Vulnerability Class**](kits/class-capability-bypass): Capability check bypasses in scripting engines represent a persistent vulnerability class where applications fail to properly enforce authorization controls when executing code through scripting interfaces.
- [**class-command-injection**](kits/class-command-injection)
- [**Isolation failures in document conversion**](kits/class-converter-isolation): Upload previews, thumbnails, and attachment rendering can hand untrusted files to interpreters that inherit the conversion worker’s operating-system permissions.
- [**File Parsing Vulnerability Class**](kits/class-file-parsing): This kit contains detection rules, check scripts, and analysis for the file parsing vulnerability class that affects image processing software.
- [**Heap Buffer Overflow Exposure Checker**](kits/class-heap-buffer-overflow): This tool detects potential heap buffer overflow vulnerabilities in software by scanning source code files for unsafe patterns that could lead to memory corruption.
- [**class-heap-overflow**](kits/class-heap-overflow)
- [**Heap Overflow Vulnerabilities: A Persistent Threat**](kits/class-heapoverflow): Heap overflow vulnerabilities represent a class of memory safety issues where data written to heap memory exceeds the allocated buffer size, potentially corrupting adjacent memory.
- [**class-incorrect-auth**](kits/class-incorrect-auth)
- [**Krita File Parsing Vulnerabilities - Class-wide Defense Kit**](kits/class-krta): This kit provides defensive measures against the pattern of file parsing vulnerabilities found in Krita.
- [**class-lua-use-after-free**](kits/class-lua-use-after-free)
- [**class-oob**](kits/class-oob)
- [**Out-of-Bounds Read Vulnerabilities in Parsers**](kits/class-oob-read): Out-of-bounds (OOB) read vulnerabilities in parsers represent a recurring class of flaws that occur when parsing functions read memory beyond the intended buffer boundaries.
- [**class-oom**](kits/class-oom)

## 🔧 Tools it built

Reusable defensive tools.

- [**CVE Sweep**](toolbox/cve-sweep): Cross-reference software inventory with local NVD CVE data and flag results listed in the CISA Known Exploited Vulnerabilities catalog. The tool reads three local JSON files and prints findings to stdout.
- [**CVE to Detection Rules Generator**](toolbox/cve-to-detection): This tool converts CVE information into Sigma and YARA detection rules for defensive purposes. It helps security teams quickly create detections for known vulnerabilities.
- [**File Parsing Tools**](toolbox/file-parsing-tools): Three read-only checks for local files before they reach a parser. Requires Python 3 on Linux and uses only the standard library. No installation is needed. Run these examples from the repository root.
- [**IOC Hash Sweep**](toolbox/ioc-hash-sweep): This tool scans a local directory recursively for files whose SHA-256 hashes match a provided list of indicators of compromise (IOCs).
- [**KEV-NVD Checker**](toolbox/kev-nvd-checker): Triage a local software inventory using the CISA Known Exploited Vulnerabilities (KEV) catalog and NVD 2.0 applicability data.

## 📚 Tools it scouted

Open-source defensive tools it read about and tried.

- [**Security Tools Catalog**](toolbox/CATALOG.md): - kits/ai-llm-jailbreak: LLM jailbreak detection system

## 📋 Lists

- [**Toolbox: Security Tools Catalog**](toolbox/TOOLS.md): - **Description**: Detects potential LLM jailbreak attempts through rule-based and LLM-assisted analysis

## Layout

- `kits/<name>/`: one folder per threat or bug class (`README.md` or `FORESIGHT.md` first, then the rules and scripts)
- `toolbox/<name>/`: tools it built, each with a README, `--help` and tests
- `toolbox/CATALOG.md`: open-source tools it scouted, with verdicts

This page is regenerated with every commit.
