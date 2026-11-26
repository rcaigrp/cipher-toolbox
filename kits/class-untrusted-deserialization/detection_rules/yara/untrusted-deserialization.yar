rule untrusted_deserialization_dotnet {
    meta:
        description = "Detects potential untrusted deserialization in .NET applications"
        author = "Cipher"
        date = "2026-11-25"
        reference = "CVE-2026-131914, class-untrusted-deserialization"
    
    strings:
        $binary_formatter = "System.Runtime.Serialization.Formatters.Binary.BinaryFormatter" ascii
        $soap_formatter = "System.Runtime.Serialization.Formatters.Soap.SoapFormatter" ascii
        $deserialize_method = "Deserialize" ascii
    
    condition:
        (any of ($*) and filesize < 10MB)
}