rule llama_cpp_rpc_server {
    meta:
        description = "Detects potential llama.cpp RPC server processes"
        author = "Cipher"
        date = "2026-11-27"
        reference = "https://nvd.nist.gov/vuln/detail/CVE-2026-137567"

    strings:
        $rpc_port = /50052/ ascii wide nocase
        $llama_cpp = /llama.cpp/ ascii wide nocase

    condition:
        (any of them)
}