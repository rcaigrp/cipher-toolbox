rule java_native_serialization_stream : deserialization java
{
    meta:
        description = "Identifies a raw Java serialization stream for trust-boundary triage"
        scope = "Extracted files and request bodies where native Java serialization is unexpected"
        limitation = "Format indicator only. Legitimate streams match. Wrapped or encoded streams require extraction first."
    strings:
        $stream_header = { AC ED 00 05 }
    condition:
        $stream_header at 0
}
