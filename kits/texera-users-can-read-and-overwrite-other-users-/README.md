# Apache Texera workflow result authorization bypass

CVE-2026-96295 is an object-level authorization bypass (CWE-639) that lets Texera users read or overwrite other users’ workflow results. Prioritize shared deployments running a release that predates the documented fix, `1.3.0-incubating`. Verify the running release before classifying exposure. [Apache advisory](https://lists.apache.org/thread/xw55mvsfcv3md2f7fjy2b2dyx2ypkv7r) · [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-96295)

## Local exposure check

Run `./check_exposure.sh --version RELEASE --port PORT --shared yes` with values from the local deployment. Use `no` or `unknown` for shared access as appropriate. The script reads local version markers and checks TCP listeners for the supplied port when `ss` is available. A version marker is an inventory clue. Confirm the active release and check proxy, container, and access settings in the deployment record. Exit codes are `0` for the documented fixed release, `1` for a potentially exposed release, and `2` for unknown status or invalid arguments.

## Mitigation

Run `./mitigate.sh` to preview the upgrade and result verification plan. To run a reviewed, deployment-specific local upgrade procedure, use `./mitigate.sh --upgrade-script /absolute/path/to/procedure --apply`. Confirm the active fixed release afterward and compare important results with trusted copies or rerun from trusted inputs. The supplied guidance identifies an upgrade. It supplies no configuration workaround to automate.

## Sigma audit rule

`detection/sigma/texera_auth_bypass.yml` flags successful workflow result reads and overwrites when independent historical permissions indicate that access should have been denied. Map the audit fields to the rule and enrich them using ownership, sharing grants, and administrative roles at the time of each event.

## YARA evidence triage

`detection/yara/texera_result_access.yar` locates the same indicators in a normalized JSON audit record. Scan one record per file or buffer. The strings can match across records in a combined file or memory dump, so review the original structured event before acting on a hit.

## Network visibility

The supplied material gives no verified request signature, and determining whether a successful operation was authorized requires actor-to-result permission context. Use application audit evidence and historical permissions for this detection. Proxy logs can help reconstruct timing and request volume. A Suricata or Snort rule based on ordinary request traffic would flag legitimate use as well.

## Hunt queries

`hunt.md` contains Splunk SPL, Microsoft KQL, and grep/jq examples for normalized audit records, plus steps to investigate potential disclosure and overwrites.

## Prepare now

Inventory shared deployments, retain audit records and historical permissions, and identify trusted copies or reproducible inputs for critical results. Apply the same object-level authorization checks to related result APIs and use audit events that identify the actor, result, operation, and outcome.
