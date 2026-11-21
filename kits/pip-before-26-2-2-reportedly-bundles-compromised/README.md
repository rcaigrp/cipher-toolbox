# pip-before-26.2.2-reportedly-bundles-compromised

This defensive kit addresses the security incident where pip versions before 26.2.2 reportedly bundled compromised eMudhra certificates, specifically the "emSign ECC Root CA - G3" intermediate CA.

## Who is exposed?

- Systems using pip versions prior to 26.2.2
- Build runners and base images that include Python with vulnerable pip
- Any environment where pip is used to install Python packages from remote indexes

## How to use

1. **check_exposure.sh** - Run on a system to verify if pip is exposed.
2. **mitigate.sh** - Run to upgrade pip to a fixed version (dry-run by default).
3. **hunt.md** - Contains detection rules and queries for identifying exposure in logs, files, or network traffic.

For more details, see the [original advisory](https://seclists.org/oss-sec/2026/q4/803) and [Python packaging announcement](https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576).