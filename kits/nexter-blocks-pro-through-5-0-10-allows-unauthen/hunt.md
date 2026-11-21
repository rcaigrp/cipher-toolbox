# WordPress administrator activity hunt

Search the full period during which public registration and an affected Nexter Blocks Pro release were both in use. Use normalized WordPress application audit events. The Sigma rule and queries expect `event_action`, `event_outcome`, `registration_source`, and `user_role`. Populate `registration_source` from trusted application context. Preserve `site_id`, `user_id`, `actor_id`, `request_id`, and `source_ip` where available.

## Splunk SPL

Set the time picker to the exposure window and substitute your WordPress audit index and sourcetype.

```spl
index=wordpress sourcetype=wordpress:audit event_action=role_assigned event_outcome=success user_role=administrator
| eval public_registration=if(registration_source="public_registration", 1, 0)
| table _time site_id user_id actor_id request_id source_ip registration_source public_registration
| sort 0 -public_registration -_time
```

## Microsoft Sentinel KQL

Replace `WordPressAudit_CL` and the field names with your normalized table mapping. Set `exposureStart` to the beginning of the affected period.

```kusto
let exposureStart = ago(30d);
WordPressAudit_CL
| where TimeGenerated >= exposureStart
| where event_action == "role_assigned" and event_outcome == "success" and user_role == "administrator"
| extend public_registration = iff(registration_source == "public_registration", 1, 0)
| project TimeGenerated, site_id, user_id, actor_id, request_id, source_ip, registration_source, public_registration
| order by public_registration desc, TimeGenerated desc
```

## Local JSON Lines audit export

Use an export bounded to the exposure window. `grep` provides a quick text shortlist. Use `jq` to confirm field values and review all successful administrator assignments, including events with unknown origins.

```bash
grep -nF 'public_registration' wordpress-audit.jsonl
jq -c 'select(.event_action == "role_assigned" and .event_outcome == "success" and .user_role == "administrator") | {timestamp, site_id, user_id, actor_id, request_id, source_ip, registration_source}' wordpress-audit.jsonl
```

## Triage

Prioritize assignments linked to public registration. Review all remaining successful administrator grants against authorized changes, including grants to existing users. Correlate request IDs with access logs where available. If audit coverage is incomplete, compare current administrator membership with a known-good inventory or backup for each site. A current account list cannot recover removed accounts or reconstruct role history. Preserve relevant records and review suspicious accounts for subsequent privileged activity.

Prepare now by retaining account creation and role assignment events with the resulting role and request ID. Review public registration handlers for user-controlled metadata writes, allowlist permitted profile fields, and keep privileged role assignment server-controlled.
