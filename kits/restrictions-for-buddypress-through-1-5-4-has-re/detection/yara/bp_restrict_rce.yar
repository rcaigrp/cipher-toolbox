rule bp_restrict_rce_detection {
    meta:
        description = "Detects potential exploitation of BuddyPress Restrict RCE vulnerability (CVE-2026-120539)"
        author = "Cipher"
        date = "2026-11-20"
        reference = "https://nvd.nist.gov/vuln/detail/CVE-2026-120539"

    strings:
        $php_eval = /eval\(.*\)/ nocase
        $php_assert = /assert\(.*\)/ nocase
        $php_exec = /exec\(.*\)/ nocase
        $php_system = /system\(.*\)/ nocase
        $php_passthru = /passthru\(.*\)/ nocase
        $bp_restrict_path = "/wp-content/plugins/bp-restrict/" nocase

    condition:
        $bp_restrict_path and (any of ($php_*))
}