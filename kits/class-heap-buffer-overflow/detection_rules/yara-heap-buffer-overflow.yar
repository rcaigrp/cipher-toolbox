rule heap_buffer_overflow_indicators {
    meta:
        description = "Detects indicators of heap buffer overflow attempts"
        author = "Patch"
        date = "2024-11-23"
        reference = "https://example.com/heap-buffer-overflow-detection"

    strings:
        $heap_alloc = "malloc(" nocase
        $heap_free = "free(" nocase
        $memcpy = "memcpy(" nocase
        $strcpy = "strcpy(" nocase
        $strncpy = "strncpy(" nocase
        $sprintf = "sprintf(" nocase
        $snprintf = "snprintf(" nocase
        $memset = "memset(" nocase
        $memmove = "memmove(" nocase
        $buffer_overflow = "buffer overflow" nocase
        $heap_overflow = "heap overflow" nocase

    condition:
        any of ($heap_alloc, $heap_free, $memcpy, $strcpy, $strncpy, $sprintf, $snprintf, $memset, $memmove, $buffer_overflow, $heap_overflow)
}