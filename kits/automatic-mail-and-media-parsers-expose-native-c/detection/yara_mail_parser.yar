rule Mail_Parser_Resource_Diagnostic_Triage
{
    meta:
        description = "Flags local diagnostic artifacts containing both a parser marker and a resource pressure marker"
    strings:
        $parser_mime = "zbateson/mail-mime-parser" ascii wide nocase
        $parser_mailpit = "mailpit" ascii wide nocase fullword
        $pressure_memory = "out of memory" ascii wide nocase
        $pressure_cpu = "cpu budget exceeded" ascii wide nocase
        $pressure_oom = "oom_kill" ascii wide nocase
    condition:
        any of ($parser_*) and any of ($pressure_*)
}
