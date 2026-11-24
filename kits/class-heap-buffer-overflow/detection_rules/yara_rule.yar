rule heap_buffer_overflow_detection {
    meta:
        description = "Detects patterns that may indicate heap buffer overflow in text parsing"
        author = "Cipher Lab Bot"
        reference = "https://github.com/cipher-lab/cve-research"

    strings:
        $overflow_pattern1 = { 48 89 D0 48 89 C2 48 89 C7 } // Generic overflow pattern
        $overflow_pattern2 = { 4C 89 F2 48 89 C7 48 89 D0 } // Buffer manipulation pattern

    condition:
        (uint16(0) == 0x0000) or ($overflow_pattern1 at 0) or ($overflow_pattern2 at 0)
}