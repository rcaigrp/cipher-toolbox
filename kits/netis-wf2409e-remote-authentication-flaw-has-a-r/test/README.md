# Local tests

From the kit directory, run `python3 -m unittest discover -s test -v`. The suite uses YARA and exercises both scripts and the inventory rule with synthetic listener output and sample text. The mitigation test checks that `--apply` exits with status 2.

If the kit's virtual environment has Sigma CLI installed, run `.venv/bin/sigma check detection/sigma/netis-wf2409e-auth-flaw.yml` from the kit directory. The Suricata example requires a Suricata installation for engine validation.
