# Netis WF2409E management exposure (CVE-2026-136136)

The supplied investigation reports that NVD lists a public exploit. Independent verification of a proof of concept, active exploitation, affected firmware versions, and a fixed firmware release remains unavailable. Prioritize inventoried WF2409E routers with management access reachable from the internet through WAN administration, forwarding, or permissive firewall policy. Confirm the exact hardware revision and installed firmware using existing records. [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-136136) · [Netis firmware support](https://www.netis-systems.com/support/downinfo.html?id=62)

## Local exposure check

Run `./check_exposure.sh` on the local host. It inventories TCP listeners on ports 80, 443, 8080, and 8443 without sending network requests. Assess the router and upstream WAN policy from existing configuration records. Firmware status remains unknown until a fixed release is verified.

## Mitigation plan

Run `./mitigate.sh` to print the management isolation and firmware verification steps. `--apply` exits with an error and leaves configuration intact because the supplied material provides no verified device-specific procedure and the local host has no confirmed enforcement role. An authorized administrator can use the printed plan at the router or upstream enforcement point.

## Sigma

`detection/sigma/netis-wf2409e-auth-flaw.yml` flags allowed traffic to inventoried management endpoints from sources outside the approved management network. This is an exposure signal.

## YARA

`detection/yara/netis-wf2409e-exploit.yar` finds Netis and WF2409E identifiers in local files or memory dumps for inventory triage.

## Suricata

`detection/netis-wf2409e-management.rules` is a placeholder rule with example addresses. Replace the documentation addresses and example ports with inventoried values before enabling. Source address is the approved management network as seen by the sensor.

## Hunt queries

`hunt.md` provides examples for Splunk SPL, Microsoft KQL, and local grep/jq to search firewall logs for allowed connections to WF2409E management endpoints from unapproved sources.