rule oob_read_detection {
    meta:
        description = "Detection of out-of-bounds read patterns in parser components"
        author = "cipher"
        date = "2026-11-22"
    strings:
        $oob_pattern_1 = "out of bounds read" ascii
        $oob_pattern_2 = "buffer overflow" ascii
    condition:
        any of them
}