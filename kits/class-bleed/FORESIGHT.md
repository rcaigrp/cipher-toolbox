# Out-of-bounds reads in untrusted-input parsers

## Pattern

Native parsers translate input-controlled lengths and offsets into memory accesses. A check can become invalid when a later stage adjusts an offset, changes units, or opens a nested record. Reads outside the intended buffer can crash the parser or disclose memory if the application sends the bytes back. Impact depends on the data flow, so assess each report individually.

- OpenSSL CVE-2014-0160 is a historical disclosure example. A missing TLS heartbeat bounds check allowed a connected peer to receive process memory. [OpenSSL advisory](https://openssl-library.org/news/secadv/20140407.txt)
- GPAC/MP4Box CVE-2026-130632 is a recent availability example. The reporter describes a VC-1 start-code offset applied twice in an MPEG-2 TS demuxing path and reports no confidentiality impact. [Reporter disclosure](https://www.openwall.com/lists/oss-security/2026/11/20/7)
- The ytnef maintainer reports that 2.1.3 fixes out-of-bounds reads and a heap overflow in TNEF parsing. The maintainer identifies Evolution, Geary and the Claws Mail TNEF plugin as examples of consumers. Confirm the installed package and enabled parsing path locally. [Maintainer disclosure](https://www.openwall.com/lists/oss-security/2026/11/20/11)

## Where to look next

| Review target | Why prioritize it | Confidence |
|---|---|---|
| GPAC transport-stream codec handlers and shared packet helpers | Neighboring handlers can adjust offsets after demuxing. Review whether every final read uses the remaining length of the current buffer. | High review priority. Additional defects unconfirmed. |
| libytnef consumers and downstream bundled copies | The same parser can be reached through automatic attachment processing, and bundled copies can lag distribution updates. | High confidence in shared exposure where libytnef is enabled. Validate each deployment. |
| FFmpeg/libavformat upload and preview workers | Native demuxers also interpret nested lengths and offsets. Prioritize automatically invoked formats and codec handoffs. | Medium confidence in design similarity. A corresponding defect is unconfirmed. [FFmpeg security index](https://ffmpeg.org/security.html) |

Format growth and compatibility paths keep adding branches that can invalidate earlier checks. Review shared cursor and slice helpers along with format-specific handlers. For code the team maintains, centralize checked reads and test boundary conditions using sanitizers and ordinary regression fixtures.

## Early warning

Track oss-security and upstream release notes for offset corrections, truncated-input checks, and remaining-length validation. Treat these as review signals pending confirmation of the affected path and impact. Use ZDI upcoming entries to flag product inventory for review. Vendor-only listings provide insufficient evidence to assign this bug class. Use AI-assisted release-note triage to group signals, with human review against upstream records before escalation. [ZDI upcoming advisories](https://www.zerodayinitiative.com/advisories/upcoming/)

## Prepare now

- Inventory which mail gateways, previews and transcoders parse external bytes automatically. Record enabled formats, linked or bundled libraries, image versions, and service owners.
- Disable unused handlers. Isolate parsers in dedicated workers with minimal privileges, no credentials, restricted filesystem access and outbound access denied by default. Bound CPU, memory and job duration.
- Record a trusted worker identity, job identifier, format and termination reason. Alert on memory-safety diagnostics and hunt for crash clusters or unexpected outbound connections. A clean crash hunt leaves silent overreads unobserved. Keep raw attachments and process memory out of routine logs.
