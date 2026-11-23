rule command_injection_patterns {
    meta:
        description = "Detects common command injection patterns"
        author = "Cipher"
        date = "2026-11-23"
    
    strings:
        $pipe = "|"
        $semicolon = ";"
        $ampersand = "&"
        $backtick = "`"
        $dollar_paren = "$("
        $dollar_bracket = "${"
    
    condition:
        any of them
}