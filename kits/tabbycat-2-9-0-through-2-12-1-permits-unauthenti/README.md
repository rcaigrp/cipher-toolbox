# Tabbycat tournament API defense kit

Tabbycat 2.9.0 through 2.12.1 reportedly allows unauthenticated tournament writes through `/api/v1/tournaments` because an authorization check fails open. Prioritize deployments where untrusted clients can reach the route, including deployments with a directly reachable application backend. The reporter confirmed that deleting a tournament also removed its teams and speakers in a default deployment. VulnCheck assigned CVSS 4.0 8.8 High. Maintainers committed a fix on `develop`. The supplied material leaves the first fixed tagged release, public exploit code, and exploitation in the wild unconfirmed. [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-135429) · [VulnCheck advisory](https://www.vulncheck.com/advisories/tabbycat-2.9.0-through-2.12.1-unauthenticated-tournament-modification-via-rest-api) · [Upstream report](https://github.com/TabbycatDebate/tabbycat/issues/3047) · [Fix commit](https://github.com/TabbycatDebate/tabbycat/commit/b7f0746ba9cb5a23f94ac169dbe5b68a5fbd1ab2)

## `check_exposure.sh`

Run `./check_exposure.sh` locally with the deployment Python active. Supply `--version X.Y.Z` if package metadata is unavailable, `--repo LOCAL_CHECKOUT` to check fix ancestry, and `--nginx-include LOCAL_FILE` to inspect the kit guard. Review the reported listeners, confirm the checkout corresponds to the running service, and verify that the active proxy includes the guard and that clients cannot bypass it. Exit 1 flags a potentially affected deployment, exit 2 means unknown version or invalid arguments, and exit 0 means the supplied checkout includes the fix or the version falls outside the reported range. Read the verdict to distinguish those cases.

## `mitigate.sh`

Preview the emergency Nginx workaround with `./mitigate.sh --nginx-include /absolute/path/to/tabbycat-guard.conf`. Add `--apply` to install the include file. The guard blocks all methods on the tournament API, including legitimate reads and integrations. Include it at server scope in each Tabbycat virtual host, validate with `nginx -t`, and reload through your normal change process. Restrict direct access to the application backend separately. This kit implements the investigation's access restriction recommendation for Nginx.

## `detect.sigma.yml`

Map the HTTP method, normalized path, client IP, and status fields to your webserver logs. Scope the rule to Tabbycat and correlate matches with request identity and audit records. Authorized writes and blocked requests can both alert.

## `detect.spl`

Run the standalone Splunk hunt after mapping the index, sourcetype, and fields to your Tabbycat logs.

## `hunt.md`

Use the Splunk SPL, Microsoft KQL, grep, or jq examples to find tournament write requests. Prioritize unexplained successful responses and reconcile them against tournament, team, and speaker records.

## `tabbycat-access-log.yar`

Run `yara tabbycat-access-log.yar test_data/access.log` to check the combined-format fixture. Use the rule to triage similar access-log files. A hit identifies a write request. Correlate it before assigning incident significance. The supplied investigation provides no memory indicators.

## `tabbycat.rules`

Load this Suricata HTTP rule on a sensor that sees decrypted traffic destined for the Tabbycat service. Set `HOME_NET` and scope deployment to the relevant service or segment. The rule alerts on request method and URI. Use application logs to determine identity, response, and impact. Validate with `suricata -T -c /etc/suricata/suricata.yaml -S "$PWD/tabbycat.rules"` before deployment.

## `test_data/access.log` and `test_data/access.json`

Synthetic combined-format and JSON Lines access logs. Each contains two write records and one GET control. Use these as local inputs for the corresponding hunt and log-rule checks.

## Prepare now

Preserve proxy and application logs, audit recent tournament changes, and verify that backups restore tournament, team, and speaker data. Review other write handlers that derive permissions from tournament or tenant context. Require explicit authorization and deny writes when that context is missing. Restrict backend access and collect method, normalized route, status, request ID, and authenticated identity for incident correlation. Track upstream reports and fixes before a release or CVE appears so the team can deploy temporary access controls early. If using AI to cluster suspicious log activity, treat request fields as untrusted input, keep the workflow read-only, and verify findings against audit records.
