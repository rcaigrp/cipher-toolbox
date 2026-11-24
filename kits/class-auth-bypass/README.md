# Authentication bypass review kit

This kit contains experimental checks and detection material for defensive review. Review the limitations below before interpreting any output.

- `FORESIGHT.md` describes common authentication control failures.
- `detection.yml` is an experimental web-log rule for successful API requests. It has no condition for missing or invalid authentication.
- `check_vmware_auth_bypass.sh` checks local processes, listeners, and configuration. Its listener filter can match unrelated ports, and its output does not establish whether VMware is affected.
- `check_exposure.py` is a prototype HTTP check. It treats HTTP 403 as potential exposure, and it can report a clean result when every connection fails.
- `fortinet/README.md` documents the Fortinet prototype and its limitations.
- `test_auth_bypass.py` uses mocked responses to check how the generic Python script handles a successful request and a connection error.

Run the offline tests from this directory with `python3 -m unittest -v test_auth_bypass`. The tests require `requests` and do not contact a service. The Python prototypes currently attempt connections when invoked with `--help`.
