rule peoplesoft_webroot_jsp_process_launch_triage {
    meta:
        description = "Triage JSP source in PeopleSoft webroots or recovered memory for servlet input and Java process launch markers"
        scope = "Behavioral heuristic for suspicious server-side artifacts; no verified CVE-specific indicators"

    strings:
        $jsp_directive = "<%@" ascii
        $jsp_expression = "<%=" ascii
        $input_parameter = "request.getParameter(" ascii
        $input_reader = "request.getReader(" ascii
        $input_stream = "request.getInputStream(" ascii
        $launch_runtime = "Runtime.getRuntime().exec(" ascii
        $launch_builder = "ProcessBuilder(" ascii

    condition:
        any of ($jsp_*) and any of ($input_*) and any of ($launch_*)
}
