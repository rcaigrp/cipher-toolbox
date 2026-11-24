# Tabbycat tournament API defense kit

Tabbycat 2.9.0 through 2.12.1 reportedly permits unauthenticated tournament writes because an authorization check fails open. Prioritize deployments where untrusted clients can reach the tournament API or connect directly to the application backend. The first fixed tagged release and exploitation in the wild remain unconfirmed in the supplied material. [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-135429) · [Upstream fix](https://github.com/TabbycatDebate/tabbycat/commit/b7f0746ba9cb5a23f94ac169dbe5b68a5fbd1ab2)

## Check local exposure

Run the executable Bash checker with the deployment's Python 3 on `PATH`. Provide the deployed version if package metadata is unavailable. Supply a local checkout to check whether it contains the upstream fix and a local Nginx include to look for the kit guard.

```sh
./check_exposure.sh --help
./check_exposure.sh --version 2.12.1
./check_exposure.sh --repo /path/to/deployed/checkout --nginx-include /path/to/guard.conf
```

Exit 1 flags potential exposure. Exit 2 indicates an unknown verdict or invalid arguments. Check the printed verdict on exit 0, since a version outside the reported range leaves fix status and reachability unverified. Confirm that the supplied checkout represents the running build, that Nginx loads the inspected include, and that network controls prevent direct backend access. Review the local TCP listeners printed by the checker.

## Preview mitigation

```sh
./mitigate.sh --nginx-include /path/to/guard.conf
```

The default dry run prints the guard and leaves the target file untouched. Review the intended effect on legitimate tournament writes before using `--apply`. Validate the active Nginx configuration and confirm the backend is reachable only through the intended proxy or trusted network.

## Review telemetry

Use `hunt.md` for Splunk, KQL, and local access-log searches. The kit includes `detection_rules/sigma_rule.yml` and `detection_rules/yara_rule.yar`. Validate each rule against your log format and correlate candidate requests with authentication and application audit records before treating a hit as an incident.

## Local verification

Run `./test_data/test_kit.sh` with `jq` installed to check the local scripts and exercise the combined-format and JSON Lines sample logs.

Run `bash -n ./check_exposure.sh` and check `--help`. With explicit inputs, the checker returned exit 1 for both affected-range boundaries (`2.9.0` and `2.12.1`), exit 0 for adjacent out-of-range inputs (`2.8.9` and `2.12.2`), and exit 2 for a prerelease input (`2.12.1rc1`) and a missing argument. A mitigation dry run left its temporary target absent. Saving the preview as a fixture let the checker recognize the guard while still reporting potential exposure for `2.12.1`. These checks used local inputs only.
