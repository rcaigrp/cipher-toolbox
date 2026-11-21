# PeopleSoft registration security kit

ZDI describes authenticated authorization bypass in the `register` operation with possible code execution as a service account on a peer. Oracle describes the same CVE as unauthenticated remote code execution in PeopleTools Updates Environment Management and names supported releases 8.61 and 8.62. The relationship between these descriptions and the exact fixed build for the `register` path remain unconfirmed in the supplied material. Mandiant reports exploitation associated with the CVE and WAF bypass. The exploited campaign path and `register`-specific indicators remain unconfirmed. Prioritize reachable management services and previously exposed systems. [ZDI](https://www.zerodayinitiative.com/advisories/ZDI-26-1039/) · [Oracle alert](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html) · [November PeopleSoft appendix](https://www.oracle.com/security-alerts/cspunov2026.html#AppendixPS) · [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-renewed-mass-exploitation-campaign-targeting-oracle-peoplesoft)

## check_exposure.sh

Run `bash check_exposure.sh --installed-version BUILD --config LOCAL_FILE` on each host. Supply the exact build from local inventory and repeat `--config` for each local domain or listener file. It reports release-family applicability, wildcard assignments and local TCP/UDP listeners. A wildcard binding alone cannot establish management-plane reachability. Exit 2 indicates unresolved fix coverage or exposure. Check the build against Oracle's deployment-specific guidance.

## mitigate.sh

Run `bash mitigate.sh` to see the patch verification and access-hardening plan. `--apply` exits 2 without changes because the supplied material lacks the deployment-specific Oracle installation and configuration instructions. Use the dry-run output to collect the build inventory, verify patch coverage and identify required administration hosts and peers before enforcing restrictions.

## detection/sigma/peoplesoft-register-cve-2026-35273.yml

Map the fields to local PeopleSoft management logs and substitute the verified route in both selectors. The rule records candidate route access for correlation with identity and host telemetry.

## detection/yara/peoplesoft-register.yar

Scan PeopleSoft webroots or authorized local memory exports for JSP markers alongside servlet input and Java process-launch strings. Review matches against known-good deployment artifacts. These are behavioral triage signals with possible legitimate matches and incomplete coverage.

## detection/suricata/peoplesoft-register.rules

Replace the illustrative route in both matches, scope the rule to PeopleSoft management destinations, and validate it with Suricata before deployment. The rule records matching requests where the sensor can see HTTP, such as after TLS termination. Expect routine traffic. Snort compatibility is unverified.

## detection/hunt.md

Map the example data sources and fields, then use the SPL, KQL, grep or jq query to find candidate route access. Correlate unusual events with peer connectivity, service-account process activity and changes to deployed web artifacts.

## Prepare now

Verify the Oracle fix for every deployment and ask Oracle to confirm ZDI-26-1039 coverage for the exact build. Audit registration privileges and peer trust, narrow management-plane access to required clients, and retain management, process and network telemetry for previously exposed hosts.
