# Isolation failures in document conversion

Upload previews, thumbnails, and attachment rendering can hand untrusted files to interpreters that inherit the conversion worker’s operating-system permissions. A failure in the interpreter’s internal sandbox can therefore put any files, credentials, or network destinations available to the worker within reach. Review the worker’s effective permissions as part of the upload surface.

## Evidence

- CVE-2024-29510 is a historical Ghostscript SAFER bypass documented by [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-29510).
- The [CNA record for CVE-2026-125396](https://www.cve.org/CVERecord?id=CVE-2026-125396) describes another Ghostscript SAFER bypass and identifies 10.08.0 as the fixed boundary for that record. Check downstream advisories for backports.
- The [oss-security thread](https://www.openwall.com/lists/oss-security/2026/11/21/2) reports that the upstream release notes initially described security fixes broadly. Compare those notes with the [vendor CVE index](https://www.ghostscript.com/releases/cve/index.html). The supplied material does not establish exploitation in the wild.

## Where to look next

- High confidence in shared exposure where ImageMagick delegates PDF or PostScript rendering to Ghostscript. Confirm the effective policy in the deployed worker and inventory the actual delegate binary. Other ImageMagick configurations can disable delegates or restrict document coders. [ImageMagick security policy](https://imagemagick.org/security-policy/)
- Medium confidence in the same isolation weakness across content-management thumbnail jobs and attachment-preview services that invoke an external renderer with the parent service identity. Verify the worker process tree, mounts, credentials, and egress. The supplied material establishes no additional affected products.
- Watch for release notes mentioning generic security fixes, restrictions on previously accepted document features, changes to delegate policy, and new disclosures naming preview or conversion components. Vendor-only ZDI entries provide too little detail to assign them to this class.

## Prepare now

Inventory which upload and attachment paths trigger conversion, which formats each path accepts, and the binaries and versions actually deployed, including inside worker images. Disable unused formats and external delegates. Move required conversions to dedicated unprivileged workers with per-job scratch space, read-only input, a dedicated output location, no application secrets or host sockets, and denied outbound access where conversion can run offline. Apply resource limits and verify controls on each worker image with ordinary input and policy tests.

Collect process ancestry, unexpected network connections, and access to sensitive paths from conversion workers. Correlate alerts with job ID, worker identity, and image version. Use controlled, benign fixtures to verify that the collector sees child processes and policy denials. Treat an alert as a lead and use the worker’s expected behavior to triage it.
