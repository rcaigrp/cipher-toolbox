rule weak_rng_usage {
    meta:
        description = "Detects usage of weak random number generation functions"
        author = "Cipher"
        date = "2026-11-28"
    
    strings:
        $rand_func = "rand()"
        $random_func = "random()"
        $srand_func = "srand()"
        $time_seed = "time()"
        $getpid_func = "getpid()"

    condition:
        any of them
}