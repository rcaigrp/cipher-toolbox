rule DotNet_Legacy_Serializer_Reference {
    meta:
        description = "Inventory legacy serializer references in managed PE artifacts for manual review"
        author = "Cipher"
    strings:
        $formatter_binary = "BinaryFormatter" fullword ascii wide
        $formatter_soap = "SoapFormatter" fullword ascii wide
        $formatter_object_state = "ObjectStateFormatter" fullword ascii wide
        $formatter_los = "LosFormatter" fullword ascii wide
        $formatter_net_data_contract = "NetDataContractSerializer" fullword ascii wide
    condition:
        uint16(0) == 0x5a4d and any of ($formatter_*)
}
