rule weak_random_usage {
    meta:
        description = "Detects usage of weak random number generation functions"
        author = "Cipher"
        date = "2026-11-28"
    strings:
        $rand = "random.randint"
        $rand_func = "rand()"
    condition:
        any of them
}