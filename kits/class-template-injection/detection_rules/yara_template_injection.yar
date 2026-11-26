rule template_injection {
    meta:
        description = "Detects potential template injection attempts"
        author = "Cipher Security Team"
        date = "2026-11-26"
        reference = "CVE-2026-XXXXX"
    
    strings:
        $template_syntax1 = "{{"
        $template_syntax2 = "${"
        $template_syntax3 = "{%"
        $template_syntax4 = "<%"
    
    condition:
        any of ($template_syntax*)
}