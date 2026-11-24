rule fuseki_shacl_ssrf_pattern {
    meta:
        description = "Detects potential SSRF patterns in Fuseki SHACL validation"
        author = "Cipher"
        date = "2026-11-25"
        reference = "https://seclists.org/oss-sec/2026/q4/853"
        hash = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

    strings:
        $http_url = /http:\/\/[^\s]+/ nocase
        $https_url = /https:\/\/[^\s]+/ nocase
        $fetch_remote = /Fetching remote resource during SHACL validation/ nocase
        $shacl_request = /SHACL validation request to/ nocase

    condition:
        any of them
}