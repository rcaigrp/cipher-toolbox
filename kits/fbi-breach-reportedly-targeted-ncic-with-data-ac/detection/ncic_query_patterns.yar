rule ncic_query_patterns {
    meta:
        description = "Detects suspicious NCIC query patterns in memory or files"
        author = "Cipher"
        date = "2026-11-22"
    
    strings:
        $query1 = "SELECT * FROM ncic_records" nocase
        $query2 = "SELECT * FROM criminal_database" nocase
        $query3 = "WHERE status = 'active'" nocase
    
    condition:
        any of them
}