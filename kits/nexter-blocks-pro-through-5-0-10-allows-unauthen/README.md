# Nexter Blocks Pro defense kit

CVE-2026-125294 allows unauthenticated administrator account creation on sites running Nexter Blocks Pro through 5.0.10 with registration enabled and a public Nexter login or registration block. The reported flaw involves different interpretations of a user metadata key by application validation and the database collation. Wordfence rates it 9.8 Critical and identifies 5.0.11 as the first patched release. Vendor confirmation of this specific fix, public PoC availability, CISA KEV status, and exploitation in the wild remain independently unverified in the supplied material. [Wordfence advisory](https://www.wordfence.com/threat-intel/vulnerabilities/id/8670d9ac-e2b0-4c19-a9d7-00be23a139c4?source=cve)

Update exposed sites to 5.0.11 or a newer patched release. If patching must wait, disable the affected plugin and audit administrator account creation and role changes across the exposure window.

## `check_exposure.py`

Run `python3 check_exposure.py --wp-root /path/to/wordpress` for each local site. Use `--plugin-dir /path/to/plugin` for a custom layout. Add `--plugin-active`, `--public-registration`, and `--public-nexter-block` with `yes`, `no`, or `unknown` based on trusted configuration or audit records. The script reads plugin headers and inventories local TCP listeners with `ss`. Site prerequisites default to unknown because their values can reside in the database. Listener addresses do not establish public reachability. Exit status `0` indicates the reported fix threshold is met or a supplied prerequisite is absent, `1` indicates all reported prerequisites are present for an affected version, and `2` indicates incomplete verification.

## `mitigate.py`

Run `python3 -B mitigate.py --plugin-dir /path/to/wp-content/plugins/nexter-blocks-pro` to preview filesystem disablement. Add `--apply` to move the verified affected plugin directory to the destination printed by the preview. The move can affect every site sharing that installation and may interrupt pages using Nexter features. Verify that WordPress no longer loads the plugin and check the affected pages. Install a patched release before re-enabling it.

## `detection/sigma/nexter_blocks_pro_priv_esc.yml`

Map WordPress application audit events to the fields documented in the rule and convert it for your SIEM. It flags successful administrator role assignments attributed to public registration. Supply registration context from trusted application telemetry and investigate matches against approved changes.

## `detection/nexter_registration_admin_audit.yar`

Run `yara detection/nexter_registration_admin_audit.yar event.json` on a single normalized JSON audit event. The rule can also triage scan buffers containing one event each. Keep events separate so fields from unrelated records cannot satisfy the same match. Use the result as an audit lead.

## `detection/wordpress_registration.rules`

Load this rule in Suricata, set `HOME_NET` to cover the WordPress servers, and place the sensor where it can see HTTP after TLS termination. The rule flags POSTs to the standard WordPress registration form for correlation with application audit events. Nexter-specific routes are unverified in the supplied material. A network hit gives request context only.

## `hunt.md`

Use the Splunk SPL, Microsoft Sentinel KQL, or local grep and jq examples over the exposure window. Review successful administrator grants against authorized changes, including grants with unknown registration origins. If historical logs are incomplete, compare current administrator membership with a known-good inventory.

## Prepare now

Retain account creation and role assignment events with resulting roles and request IDs. Review other WordPress registration and profile handlers that write user metadata. Allowlist permitted profile fields and keep privileged role assignment server-controlled.
