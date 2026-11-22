rule Assistant_Web_Context_Unapproved_Sensitive_Read_Audit {
    meta:
        description = "Triage normalized assistant gateway audit exports in files or memory"
        scope = "Metadata heuristic for one JSON audit record per scanned object"

    strings:
        $event = /"event_type"[ \t]*:[ \t]*"assistant_tool_access"/
        $context = /"context_source"[ \t]*:[ \t]*"web_content"/
        $resource = /"resource_type"[ \t]*:[ \t]*"(chat_history|saved_memory)"/
        $outcome = /"outcome"[ \t]*:[ \t]*"allowed"/
        $approval = /"approval_status"[ \t]*:[ \t]*"(missing|denied|unknown)"/

    condition:
        all of them
}
