rule SurrealDB_Possible_Embedded_Script_Artifact {
    meta:
        description = "Triage heuristic for SurrealQL artifacts and memory fragments"
        reference = "CVE-2026-134292"
    strings:
        $query = /\b(RETURN|SELECT|LET)\b/ nocase
        $script = /\bfunction[ \t\r\n]*\([^)]{0,128}\)[ \t\r\n]*\{/ nocase
    condition:
        $script and $query in (@script - 128 .. @script)
}
