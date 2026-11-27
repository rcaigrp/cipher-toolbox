rule budibase_filter_erasure_indicators {
    meta:
        description = "Indicators of Budibase filter erasure vulnerability (CVE-2026-137498)"
        author = "Cipher"
        date = "2026-11-26"
        reference = "https://nvd.nist.gov/vuln/detail/CVE-2026-137498"

    strings:
        $filter_empty = "{ \"filter\": {} }" nocase
        $public_query = "/api/public/query" nocase

    condition:
        $filter_empty and $public_query
}