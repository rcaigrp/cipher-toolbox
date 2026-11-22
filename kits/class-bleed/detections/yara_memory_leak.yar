rule parser_worker_asan_out_of_bounds_read_report {
    meta:
        description = "Matches AddressSanitizer out-of-bounds read reports collected from trusted parser worker stderr"
    strings:
        $bounds_heap = "ERROR: AddressSanitizer: heap-buffer-overflow"
        $bounds_stack = "ERROR: AddressSanitizer: stack-buffer-overflow"
        $bounds_global = "ERROR: AddressSanitizer: global-buffer-overflow"
        $read = "READ of size "
    condition:
        any of ($bounds_*) and $read
}
