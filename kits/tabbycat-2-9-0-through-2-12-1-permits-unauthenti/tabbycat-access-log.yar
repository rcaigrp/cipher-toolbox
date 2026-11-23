rule Tabbycat_Tournament_API_Write_In_Access_Log
{
    meta:
        description = "Triage combined-format HTTP access log files for tournament API write requests"
        reference = "https://nvd.nist.gov/vuln/detail/CVE-2026-135429"
    strings:
        $request = /"(POST|PUT|PATCH|DELETE) \/api\/v1\/tournaments([\/?][^" \r\n]*)? HTTP\/[0-9.]+" [1-5][0-9][0-9] /
    condition:
        $request
}
