rule tabbycat_unauth_tournament_mod {
    meta:
        description = "Detects unauthenticated tournament modification in Tabbycat"
        author = "Cipher"
        date = "2026-11-24"
        reference = "CVE-2026-135429"
        category = "web"
        malwareremoved = false

    strings:
        $post_method = "POST /api/v1/tournaments" ascii
        $tabbycat_ua = "Tabbycat" ascii

    condition:
        $post_method and $tabbycat_ua
}