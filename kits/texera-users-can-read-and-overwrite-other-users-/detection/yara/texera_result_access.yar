rule Texera_Workflow_Result_Access_Despite_Expected_Denial
{
    meta:
        description = "Flags normalized Texera audit evidence of a successful result read or overwrite despite independently determined denial"
        reference = "https://www.cve.org/CVERecord?id=CVE-2026-96295"
        scope = "One normalized JSON audit record per file or buffer. Use the hunt queries for multi-record logs."

    strings:
        $resource = /"resource_type"[ \t\r\n]*:[ \t\r\n]*"workflow_result"/
        $operation = /"operation"[ \t\r\n]*:[ \t\r\n]*"(read|overwrite)"/
        $outcome = /"outcome"[ \t\r\n]*:[ \t\r\n]*"success"/
        $permission = /"expected_access"[ \t\r\n]*:[ \t\r\n]*"denied"/

    condition:
        all of them
}
