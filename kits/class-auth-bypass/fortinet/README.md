# Fortinet authentication review

The Fortinet-specific script, `check_fortinet_auth.py`, is an unverified prototype. It makes HTTPS requests even when passed `--help`, disables certificate verification, and can report a clean result when every connection fails. Its output is insufficient to establish whether a device is affected by an authentication bypass.

The kit-wide experimental web-log rule is in `../detection.yml`. It matches successful API requests and does not establish whether those requests were authenticated.
