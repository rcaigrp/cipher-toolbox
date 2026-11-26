rule legacy_aspnet_auth_bypass {
    meta:
        description = "Detects potential authentication bypass attempts in legacy ASP.NET applications"
        author = "Cipher"
        date = "2026-11-26"
        reference = "CVE-2026-131914"

    strings:
        $cookie_pattern = /ASPXAUTH=[A-Za-z0-9+\/=]+/
        $form_data = /__VIEWSTATE=[A-Za-z0-9+\/=]+/
        $legacy_serialization = /BinaryFormatter|SoapFormatter/

    condition:
        ($cookie_pattern and $form_data) or $legacy_serialization
}
