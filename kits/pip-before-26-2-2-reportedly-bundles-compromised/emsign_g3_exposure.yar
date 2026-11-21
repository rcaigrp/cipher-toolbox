rule Emsign_Ecc_Root_G3_Exposure_Indicator
{
    meta:
        description = "Flags the emSign ECC Root CA - G3 name in a trust bundle or certificate artifact. The name alone does not establish chain acceptance or exploitation."
        reference = "https://github.com/advisories/ghsa-6q48-6c7w-9gw2"
    strings:
        $root_name = "emSign ECC Root CA - G3" ascii wide
    condition:
        $root_name
}
