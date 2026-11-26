rule unauth_rce_installer {
    meta:
        description = "Detects potential unauthenticated RCE in web application installers"
        author = "Cipher"
        date = "2026-11-26"
        reference = "CVE-2026-132165, CVE-2026-69178, CVE-2026-69179"
    
    strings:
        $install_path = "/install" ascii
        $setup_path = "/setup" ascii
        $rce_pattern = "system(" ascii nocase
        $exec_pattern = "exec(" ascii nocase
    
    condition:
        any of them
}