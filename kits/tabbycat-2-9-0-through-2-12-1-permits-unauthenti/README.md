# Tabbycat tournament API defense kit

Tabbycat 2.9.0 through 2.12.1 is reported to permit unauthenticated tournament writes through `/api/v1/tournaments` when an authorization check fails open. Deployments that allow untrusted clients to reach the endpoint are exposed. The original reporter confirmed that tournament deletion also removed teams and speakers in a default deployment. VulnCheck scored the issue 8.8 High under CVSS 4.0. A tagged release containing the upstream fix, public exploit code, and exploitation in the wild remain unconfirmed in the supplied material. [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-135429) · [VulnCheck advisory](https://www.vulncheck.com/advisories/tabbycat-2.9.0-through-2.12.1-unauthenticated-tournament-modification-via-rest-api) · [Upstream report](https://github.com/TabbycatDebate/tabbycat/issues/3047) · [Fix commit](https://github.com/TabbycatDebate/tabbycat/commit/b7f0746ba9cb5a23f94ac169dbe5b68a5fbd1ab2)

## `check_exposure.sh`

Run `./check_exposure.sh` on the deployment host with its Python environment active. Pass `--version X.Y.Z` if the installed metadata is unavailable, `--repo LOCAL_CHECKOUT` to verify upstream fix ancestry, and `--nginx-include LOCAL_FILE` to inspect the kit guard. The script reads local state and lists TCP listeners using `ss`. Exit 1 flags a reported affected version, exit 2 means the version is unknown or the arguments are invalid, and exit 0 means the supplied checkout includes the fix or the version is outside the reported range. Verify that the running build corresponds to the checkout, that the proxy loads the guard, and that the backend is unreachable directly from untrusted networks.

## `mitigate.sh`

Preview the emergency Nginx block with `./mitigate.sh --nginx-include /absolute/path/to/tabbycat-guard.conf`. Add `--apply` to install the include at that path without overwriting an existing file. Include it at server scope in every Tabbycat virtual host, run `nginx -t`, then reload Nginx. Restrict direct backend access separately. This implements the reported recommendation to restrict access and returns 403 for the tournament API, including its read operations. To roll back, remove the include directive, validate and reload Nginx, then remove the generated file.

## `detect.sigma.yml`

Scope the rule to Tabbycat access logs and map the method, normalized path, status, and source IP to your logging fields. It flags write requests for correlation with authentication and audit records.

## `tabbycat-access-log.yar`

Run `yara tabbycat-access-log.yar access.log` against local combined-format access logs. A match identifies a file containing a tournament API write request. The supplied material provides no memory indicators.

## `tabbycat.rules`

Load the rule in Suricata on a sensor that can see decoded HTTP, such as the cleartext side of a TLS-terminating proxy. Scope the destination to the Tabbycat backend in your local deployment. A match identifies a write request regardless of authorization or outcome.

## `hunt.md`

Use the SPL, KQL, grep, or jq examples with Tabbycat access logs. Correlate request IDs, authenticated identities, response statuses, and application audit records. Investigate unexplained successful writes and check for related tournament, team, or speaker changes.

## Prepare now

Preserve proxy and application logs, audit unexpected changes, and verify recovery backups cover tournaments, teams, and speakers. Review similar collection and detail endpoints for permission checks that default to allowing writes when tournament context is missing. Require explicit write authorization and test missing-context cases in the application authorization layer.
