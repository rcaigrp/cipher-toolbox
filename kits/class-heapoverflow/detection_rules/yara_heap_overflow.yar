rule HeapOverflowPattern {
    meta:
        description = "Detects potential heap overflow patterns in memory dumps"
        author = "Cipher"
        date = "2026-11-21"

    strings:
        $heap_overflow = { 48 89 5C 24 ?? 48 89 74 24 ?? 57 48 83 EC 20 }
    condition:
        $heap_overflow
}