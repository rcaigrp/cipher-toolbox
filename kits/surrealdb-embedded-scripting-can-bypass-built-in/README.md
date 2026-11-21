# SurrealDB embedded scripting authorization bypass

Embedded JavaScript can bypass restrictions on built-in functions. The supplied advisories report the affected range as 1.0.0 up to, but excluding, 4.0.0. Prioritize deployments with scripting enabled. Unauthenticated exposure, public proof-of-concept code, and exploitation in the wild are unconfirmed. Upgrade to the reported fixed release, 4.0.0, and disable scripting where feasible pending rollout. [Vendor advisory](https://github.com/surrealdb/surrealdb/security/advisories/GHSA-5w6j-qm42-4rc2) · [4.0.0 release](https://github.com/surrealdb/surrealdb/releases/tag/v4.0.0)

## Local exposure check

Run `python3 check_exposure.py` on the SurrealDB host. It reports the PATH binary version, visible native server processes, scripting flags, and attributable local TCP listeners. Review deployment configuration, containers, and embedded instances separately. Missing flags leave the effective policy unknown.

## Mitigation

Run `python3 mitigate.py --unit surrealdb.service` to preview a scripting-denial override for a simple native systemd service. Add `--apply` with appropriate local privileges to install the override. Activate it with `systemctl daemon-reload` and a planned restart of that unit. Rerun the exposure check and verify the effective scripting policy. For rollback, remove the generated `90-deny-scripting.conf`, reload systemd, and restart the unit during an approved window. Review complex units and deployments that enable scripting through broad capability flags before changing them.

## Sigma

`detection/sigma/surrealdb_scripting_bypass.yml` flags logging that mentions scripting alongside capability or permission decisions. Route SurrealDB logs to this rule and map the rendered event text to `message`.

## YARA

`detection/yara/surrealdb_scripting.yar` flags script-shaped text near query keywords in artifacts or memory extracts. Limit scans to SurrealDB-related data and investigate matches in context.

## Suricata

`detection/suricata/surrealdb_scripting.rules` flags possible embedded scripting in visible HTTP POST requests to `/sql`. Scope deployment to known SurrealDB destinations. Coverage depends on HTTP body visibility and inspection depth.

## Hunts

`detection/hunt.md` contains SPL, KQL, and local command-line queries. Adapt field names and begin with a baseline of expected scripting activity. Treat all kit matches as triage leads. The supplied material provides no confirmed exploitation indicators.

Review whether scripting runtimes and extension interfaces enforce the same permissions as the main query interface. Prepare to disable optional scripting and retain policy-decision telemetry across those interfaces.
