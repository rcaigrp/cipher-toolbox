rule OpenIMIS_ReportBro_Preview_Triage
{
    meta:
        description = "Identifies openIMIS ReportBro preview context in files or memory for incident triage"
        author = "Cipher"
        reference = "https://nvd.nist.gov/vuln/detail/CVE-2026-82489"
        interpretation = "Expected in legitimate application artifacts. A match does not establish exploitation."

    strings:
        $product = "openimis" ascii wide nocase
        $renderer = "reportbro" ascii wide nocase
        $operation = "preview" ascii wide nocase

    condition:
        all of them
}