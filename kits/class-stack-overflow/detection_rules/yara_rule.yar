rule stack_overflow_detection {
    meta:
        description = "Detects patterns in logs indicating potential stack overflow from parsing"
        author = "Cipher"
        date = "2026-11-24"

    strings:
        $stack_exceeded = "stack overflow"
        $recursion_limit = "recursion limit exceeded"
        $deep_nesting = "deeply nested structure"

    condition:
        any of them
}