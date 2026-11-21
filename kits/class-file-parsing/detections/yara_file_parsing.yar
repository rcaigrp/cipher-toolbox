rule file_parsing_vuln {
    meta:
        description = "Detection for generic file parsing vulnerabilities"
        author = "Cipher"
        date = "2026-11-20"
    strings:
        $file_format_check = "File format validation failed" nocase
        $buffer_overflow = "Buffer overflow detected" nocase
    condition:
        1 of them
}