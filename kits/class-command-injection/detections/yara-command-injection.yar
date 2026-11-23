rule command_injection_patterns {
    strings:
        $pipe = /;.*\|/
        $semicolon = /;.*;/
        $ampersand = /;.*&/
        $backtick = /`[^`]*`/
        $double_ampersand = /&&/
        $double_pipe = /\|\|/

    condition:
        any of them
}