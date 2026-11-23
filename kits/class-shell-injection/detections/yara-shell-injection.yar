rule shell_injection_pattern {
    strings:
        $backtick = /`[^`]*`/
        $dollar_paren = /\$\([^)]*\)/
        $semicolon = /;.*;/
        $pipe = /;.*\|/
        $ampersand = /;.*&/
        $double_ampersand = /&&/

    condition:
        any of them
}