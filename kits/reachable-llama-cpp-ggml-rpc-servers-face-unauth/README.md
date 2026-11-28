# Reachable llama.cpp RPC Servers Face Unauthenticated RCE Risk

This defensive kit addresses CVE-2026-137567, an out-of-bounds write vulnerability in the llama.cpp RPC server that can lead to unauthenticated remote code execution when the RPC service is reachable over the network.

## What This Kit Contains

- **Detection rules**: Sigma, YARA, and Suricata rules for identifying potentially vulnerable RPC servers
- **Hunt queries**: Queries to search logs and system state for exposed RPC services
- **Exposure check script**: A script that checks if llama.cpp is installed, what version it is, and whether any RPC server is exposed over the network
- **Mitigation script**: A script that implements vendor-recommended hardening steps (upgrade to b12658+, restrict RPC access)

## Who Is Exposed

Systems running llama.cpp with an RPC server configured to listen on a non-local address (e.g., 0.0.0.0:50052) are exposed to this vulnerability.

## How to Use

1. Run `check_exposure.sh` to determine if your system is exposed
2. Review the output and decide whether to apply mitigations with `mitigate.sh --apply`
3. Deploy detection rules in your security infrastructure
4. Use hunt queries for proactive hunting of exposed RPC servers on your network
