# Local tests

From the kit directory, run `python3 -m pytest test/test_kit.py -v`. The suite checks both exposure scripts with synthetic local listener output and verifies the mitigation dry run and the `--apply` exit status. The listener fixtures cover empty output, loopback and non-loopback bindings, and an `ss` failure.

If the kit's virtual environment has Sigma CLI installed, run `.venv/bin/sigma check detection/sigma/netis-wf2409e-auth-flaw.yml` from the kit directory. The Suricata example requires a Suricata installation for engine validation.
