rule heap_buffer_overflow_pattern {
    meta:
        description = "Pattern matching for heap buffer overflow in file parsers"
        author = "Cipher"
        date = "2026-11-24"
    
    strings:
        $heap_alloc = { 89 54 24 10 48 8B 4C 24 20 }
        $buffer_copy = { 48 89 74 24 18 48 8B 4C 24 20 }
    
    condition:
        any of them
}