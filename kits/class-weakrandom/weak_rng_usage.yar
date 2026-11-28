rule weak_rng_usage {
    meta:
        description = "Detects usage of potentially weak random number generators"
        author = "Cipher"
        date = "2026-11-27"
    
    strings:
        $rand_call = /rand\(\)/ nocase
        $random_call = /random\(\)/ nocase
        $srand_call = /srand\(\)/ nocase
    
    condition:
        any of them
}