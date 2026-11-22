rule oob_read_pattern {
    meta:
        description = "Detects out-of-bounds read patterns in parser libraries"
        author = "Cipher"
        reference = "kits/class-oob-read/FORESIGHT.md"
    
    strings:
        $pattern1 = { 48 89 5C 24 ?? 48 89 74 24 ?? 48 89 7C 24 ?? 48 8B 74 24 ?? }
        $pattern2 = { 48 8B 0D ?? ?? ?? ?? 48 85 C9 74 ?? 48 8B 11 }
    
    condition:
        any of them
}