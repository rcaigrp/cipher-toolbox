rule tabbycat_unauth_tournament_api {
    meta:
        description = "Detects unauthorized access to Tabbycat tournament API endpoint"
        author = "Cipher"
        date = "2026-11-24"
        reference = "CVE-2026-135429"
        category = "web_exploitation"

    strings:
        $api_path = "/api/v1/tournaments" nocase
        $http_200 = "HTTP/1.1 200" nocase

    condition:
        $api_path and $http_200
}