rule parser_oob_read_indicators {
    meta:
        description = "Indicates potential OOB read in parsers"
        author = "Cipher"
        date = "2026-11-22"

    strings:
        $parser_call = "parse_"
        $buffer_check = "memcpy" or "strncpy" or "memmove"
        $bounds_check = "strlen" or "sizeof" or "length"

    condition:
        $parser_call and ($buffer_check or $bounds_check)
}