rule shell_injection_pattern {
    meta:
        description = "Detects potential shell injection patterns in command strings"
        author = "Cipher"
        date = "2026-11-23"
        reference = "https://example.com/shell-injection-patterns"

    strings:
        $backtick = /`.*`/
        $dollar_paren = /\$\(.*\)/
        $semicolon = /;/
        $pipe = /\|/
        $ampersand = /&/
        $double_pipe = /&&/
        $double_ampersand = /||/

    condition:
        any of them
}