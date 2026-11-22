rule OutOfBoundsReadDetection {
    meta:
        description = "Detects OOB read patterns in parser components"
        author = "Cipher"
        date = "2026-11-22"

    strings:
        $oob_read = "out-of-bounds read" nocase
        $buffer_access = "buffer access violation" nocase

    condition:
        any of them
}