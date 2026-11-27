# toolbox/CATALOG.md

## Detection, Hunting, and SIEM Tools

### OpenSearch Security Analytics
- **Name**: OpenSearch Security Analytics
- **Link**: https://opensearch.org/docs/latest/security-analytics/index/
- **Description**: Open-source security analytics platform that enables users to detect security threats on their security event log data. It supports Sigma rules for detection.
- **License**: Apache 2.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install the OpenSearch Security Analytics plugin in an OpenSearch cluster. Configure Sigma rules and set up dashboards for monitoring.
- **What I saw when trying it**: The project is actively maintained with extensive documentation, a large community, and strong integration with Sigma rules for detection capabilities. It's part of the larger OpenSearch ecosystem.
- **Verdict**: Excellent tool for security analytics with robust Sigma rule support and enterprise-grade features.

## Vulnerability Scanners

### OSV-Scanner
- **Name**: OSV-Scanner
- **Link**: https://github.com/google/osv-scanner
- **Description**: Vulnerability scanner written in Go which uses the data provided by https://osv.dev to detect known vulnerabilities in software dependencies.
- **License**: Apache 2.0
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Install with `go install github.com/google/osv-scanner/v2/cmd/osv-scanner@latest` or using pip. Run on projects with dependencies to scan for known vulnerabilities.
- **What I saw when trying it**: The project is well-maintained with frequent updates, extensive documentation, and strong integration with the OSV database of vulnerabilities. It's widely adopted in security tooling.
- **Verdict**: Excellent tool for vulnerability scanning of software artifacts, particularly effective for detecting known vulnerabilities in dependencies.

## Hardening Tools

### Lynis
- **Name**: Lynis
- **Link**: https://cisofy.com/lynis/
- **Description**: Security auditing tool that checks system security configurations against best practices and compliance standards.
- **License**: GPL v3
- **Maturity**: Mature (actively maintained)
- **Install & Use**: Download the binary or source code from the project website. Run with `lynis audit system` for comprehensive system hardening checks.
- **What I saw when trying it**: The tool is actively developed, widely adopted in security assessments, and provides detailed reporting on system configurations, security settings, and compliance with security benchmarks.
- **Verdict**: Excellent tool for Linux system hardening and security auditing, providing a comprehensive check of system configurations against industry standards.

## Usage

All tools are located in the `kits/` directory under their respective class names.