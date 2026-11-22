rule nginx_worker_sigsegv_log_artifact {
    meta:
        description = "Triage indicator for text logs and artifacts retaining an nginx worker SIGSEGV message"
        scope = "Generic worker crash telemetry; correlate with local HTTP/2 configuration and package coverage"
        reference = "https://www.cve.org/CVERecord?id=CVE-2026-123007"
    strings:
        $crash = /worker process [0-9]+ exited on signal 11([^0-9]|$)/ ascii
    condition:
        $crash
}
