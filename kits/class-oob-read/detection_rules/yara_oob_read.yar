rule oob_read_pattern {
    meta:
        description = "Detects potential OOB read patterns in binaries"
        author = "Cipher"
        date = "2026-11-22"
    strings:
        $pattern1 = {8b 4c 24 08 89 41 04} // Example pattern
        $pattern2 = {48 89 5c 24 10 48 89 74 24 18} // Another example
    condition:
        (any of them)
}