# .NET untrusted deserialization exposure review

Run `./check_exposure.sh --help` for usage. Run `./check_exposure.sh /path/to/project` to scan local files, or omit the directory to scan the current directory. The checker requires Bash, `find`, `grep`, and `strings`. It reads C# source, `web.config` and `app.config`, and strings in DLL and EXE files for potential exposure indicators. Review findings in application context. A completed scan exits 0 even when it reports findings.

## Sample check

From this directory, run `bash -n check_exposure.sh` and `./check_exposure.sh test_files`. Expect a configuration finding for `test_files/web.config` and a source finding for `test_files/test_vulnerable_code.cs`. Expect no finding for `test_files/test_safe_code.cs`. The checker reads the fixtures as data.

## Kit files

- `FORESIGHT.md` contains background and review priorities.
- `detection_rules/sigma/untrusted-deserialization.yml` contains a Sigma rule.
- `detection_rules/suricata/untrusted-deserialization.rules` contains a Suricata rule.
- `detection_rules/yara/untrusted-deserialization.yar` contains a YARA rule.
