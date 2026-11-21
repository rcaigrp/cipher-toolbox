# GPGME Data Exposure Vulnerability (CVE-2026-129975)

This defensive kit addresses a critical vulnerability in GPGME (GnuPG Made Easy) where crafted OpenPGP keys can cause a double-free condition and expose data from applications using the library.

## Who is exposed?
- Systems using GPGME 2.3.0 or earlier
- Applications that process externally supplied OpenPGP keys or signed data
- Unattended services processing untrusted input

## Files in this kit:
- `check_exposure.sh`: Checks if this system is vulnerable
- `mitigate.sh`: Applies hardening/workarounds (dry-run by default)
- `detect.sigma.yml`: Sigma rules for detecting exploitation attempts
- `hunt.md`: Hunting queries to detect potential exposure