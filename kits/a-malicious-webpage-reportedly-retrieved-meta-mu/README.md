# Meta Muse webpage-driven data exposure

A public report describes a lab demo in which a malicious webpage reportedly retrieved Meta Muse chats and saved memories. NebuSec reports that the Muse team patched the weaknesses before disclosure. The supplied material includes no independent confirmation from Meta, affected or fixed versions, or evidence of exploitation in the wild. [Incident report](https://thehackernews.com/2026/11/a-single-malicious-webpage-let.html) · [NebuSec research](https://nebusec.ai/research/meta-muse-credential-exposure/)

Review browsing assistants that can read private history or saved memories. The same trust-boundary failure can affect assistants with access to private mail, documents, or other connected data. The detections use a local audit schema and require telemetry from a gateway you control.

## `detections/sigma/web_credential_exposure.yml`

Map trusted gateway audit events to the fields in `hunt.md`, then deploy the experimental rule through your Sigma backend. It flags successful reads of chat history or saved memories in a web browsing context with missing, denied, or unverifiable approval.

## `detections/yara/muse_exposure.yar`

Run `yara detections/yara/muse_exposure.yar event.json` on a single normalized JSON audit record. If scanning a memory export, confirm that all matched fields belong to the same event before escalating. This heuristic uses audit metadata and may match unrelated records in a larger buffer.

## `detections/suricata/muse_web_access.rules`

Scope this rule to trusted gateway-to-collector traffic where Suricata already has visibility into HTTP request bodies. It expects one compact JSON event per POST to `/assistant-audit`. If you change the collector path, update the `bsize` value to match its byte length. Keep existing transport encryption in place. Use gateway logs where request bodies are encrypted or unavailable.

## `hunt.md`

Use the SPL, KQL, or jq query against normalized audit events. Correlate matches with the approval record and subsequent outbound activity to determine whether private data left the assistant.

## `check_exposure.sh`

Run `./check_exposure.sh` to inventory local TCP and UDP listeners. The script reports Muse exposure as unknown and the approval policy as unverified because the supplied material identifies neither a local product or policy location nor a fixed version.

## `mitigate.sh`

Run `./mitigate.sh` for the dry-run hardening steps. The supplied material provides no documented Meta setting or local gateway configuration, so `--apply` exits with status 3 and makes no changes. Implement the approval gate in the gateway you administer.

## Prepare now

Require explicit user approval bound to the current resource and operation before a browsing assistant can read private history or memories. Where the gateway cannot enforce that control, remove those permissions from browsing sessions. Verify denial when approval is absent, denied, expired, or mismatched, and retain decision metadata without logging private content.
