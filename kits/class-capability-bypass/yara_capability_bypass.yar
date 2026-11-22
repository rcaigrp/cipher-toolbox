rule scripting_capability_bypass {
    meta:
        description = "Indicates potential capability bypass in scripting engines"
        author = "Cipher"
        date = "2026-11-22"

    strings:
        $script_bridge = "surrealdb.functions"
        $direct_call = "fnc::synchronous" or "fnc::asynchronous"
        $capability_check = "check_function_capability" or "authorize_function"

    condition:
        $script_bridge and ($direct_call and not $capability_check)
}