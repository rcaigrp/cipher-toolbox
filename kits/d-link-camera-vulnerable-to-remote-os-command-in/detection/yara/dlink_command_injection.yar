rule dlink_recording_configuration_endpoint_artifact {
    meta:
        description = "Triage lead for the affected CGI path in camera artifacts or HTTP captures"
        reference = "CVE-2026-133680"
    strings:
        $endpoint = "/cgi-bin/localrecording/setconf.cgi" ascii wide
    condition:
        $endpoint
}
