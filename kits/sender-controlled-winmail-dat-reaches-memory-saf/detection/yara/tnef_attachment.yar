rule TNEF_Attachment_At_File_Start
{
    meta:
        description = "Identifies decoded TNEF containers for attachment triage; matches benign TNEF too"
    strings:
        $signature = { 78 9F 3E 22 }
    condition:
        $signature at 0
}

rule TNEF_Container_In_Parser_Memory
{
    meta:
        description = "Triage for TNEF bytes in a targeted parser dump; four-byte matches can be coincidental"
    strings:
        $signature = { 78 9F 3E 22 }
    condition:
        $signature
}
