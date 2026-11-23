rule out_of_bounds_read_detection {
    meta:
        description = "Detects potential OOB read patterns in parser code"
        author = "Cipher"
        date = "2026-11-22"

    strings:
        $pattern1 = { 8B 44 24 ?? 89 45 ?? 8B 4C 24 ?? }
        $pattern2 = { 8D 4C 24 ?? 89 4D ?? 8B 54 24 ?? }

    condition:
        any of them
}