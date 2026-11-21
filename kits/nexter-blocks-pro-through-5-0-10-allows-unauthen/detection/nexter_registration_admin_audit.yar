rule WordPress_Public_Registration_Admin_Assignment_Audit
{
    meta:
        description = "Triage a single normalized WordPress audit event for successful administrator assignment during public registration"
        scope = "One JSON event per file or scan buffer"
        reference = "CVE-2026-125294"

    strings:
        $action = /"event_action"[ \t]*:[ \t]*"role_assigned"/
        $outcome = /"event_outcome"[ \t]*:[ \t]*"success"/
        $source = /"registration_source"[ \t]*:[ \t]*"public_registration"/
        $role = /"user_role"[ \t]*:[ \t]*"administrator"/

    condition:
        filesize <= 65536 and all of them
}
