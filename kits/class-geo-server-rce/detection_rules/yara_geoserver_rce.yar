rule GeoServer_WMS_RCE {
    meta:
        description = "Detects GeoServer WMS requests with suspicious parameters"
        author = "Cipher"
        date = "2026-11-26"

    strings:
        $wms_path = "/geoserver/wms"
        $request_param = "REQUEST="
        $layers_param = "LAYERS="

    condition:
        $wms_path and ($request_param or $layers_param)
}