# Legacy ASP.NET exposure review

Run `./check_exposure.sh --help` for usage. Run `./check_exposure.sh /path/to/project` to scan local project files, or omit the directory to scan the current directory. The checker reads files without modifying them. Findings are inventory leads and require review of the deployed application and dependencies. A completed scan exits 0 even when it reports findings.

## Sample check

From this directory, run `bash -n check_exposure.sh` and `./check_exposure.sh test_files`. Expect one Idunno.AntiCsrf reference in `test_vulnerable_config.xml` and cookieless session indicators in both XML samples. The sample directory contains no WebForms pages or C# code.

## Kit files

- `FORESIGHT.md` contains background and review priorities.
- `detection_rules/sigma/legacy-aspnet-auth-bypass.yml` contains a Sigma rule.
- `detection_rules/suricata/legacy-aspnet-auth-bypass.rules` contains a Suricata rule.
- `detection_rules/yara/legacy-aspnet-auth-bypass.yar` contains a YARA rule.
- `test_files/test_vulnerable_config.xml` and `test_files/test_web_config.xml` contain sample configurations.

The detection rules use broad heuristics and can match ordinary ASP.NET activity. Validate and tune them against your own telemetry before deployment.
