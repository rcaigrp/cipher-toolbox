Rustinel - Endpoint Detection Engine
## Rustinel
- **Description**: Cross-platform endpoint detection engine using Sigma, YARA, and IOC rules on native telemetry
- **Link**: https://github.com/Karib0u/rustinel
- **License**: Apache License 2.0
- **Maturity**: Mature (actively maintained, v1.11.0 released in 2026)
- **Installation**: Download binary from https://rustinel.io/install.sh or GitHub releases page
- **Usage**: Run with elevated privileges to monitor system events and detect threats using Sigma rules, YARA rules, and IOC lists. Can replay recordings offline for rule testing.
- **Tested on**: Cipher's test environment with Linux x86_64 (eBPF support failed due to kernel version but config and rules loaded)
- **Verdict**: A promising, high-performance EDR solution with a strong focus on Sigma and YARA rule support. While eBPF detection failed in this test environment, the core functionality including rule loading and configuration is working.
