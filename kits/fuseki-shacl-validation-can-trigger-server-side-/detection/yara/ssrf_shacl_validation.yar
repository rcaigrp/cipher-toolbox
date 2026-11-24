rule fuseki_shacl_ssrf {
    meta:
        description = "Detects potential Fuseki SHACL SSRF patterns"
        author = "Cipher Kit"
        date = "2026-11-24"
        reference = "CVE-2026-86155"

    strings:
        $http = "http://"
        $https = "https://"
        $shacl = "/shacl"

    condition:
        any of them
}