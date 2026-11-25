rule out_of_bounds_read_pattern {
    meta:
        description = "Detects potential out-of-bounds read patterns in binary files"
        author = "Cipher"
        date = "2026-11-25"
    
    strings:
        $oob_read_1 = { 48 89 D0 48 8B 48 08 48 3B 48 10 }
        $oob_read_2 = { 4C 8B 51 08 48 8B 02 48 3B C2 }
    
    condition:
        any of them
}