# Predictable randomness in security tokens

Password reset links, invitations, recovery codes, and session identifiers rely on values that an unauthorized party cannot predict. General-purpose PRNGs and values derived from public inputs can undermine that guarantee. Hashing predictable inputs preserves their predictability.

## Evidence

- A CPAN Security Group disclosure reports predictable output in Strong::Random through 0.96 (CVE-2026-122093). The prior review found 0.96 in the MetaCPAN release listing. A fixed release and exploitation status remain unverified. [oss-security disclosure](https://www.openwall.com/lists/oss-security/2026/11/27/4), [MetaCPAN release listing](https://metacpan.org/dist/Strong-Random)
- Apache disclosed predictable password reset tokens in OpenMeetings 1.9.x through 3.1.0 and recommended upgrading to 3.1.1. [Apache disclosure](https://www.openwall.com/lists/oss-security/2016/03/25/1)
- The advisory for FIWARE Keyrock reports predictable password reset tokens through 8.4 and lists the patched version as unknown. [CVE-2024-42163 advisory record](https://github.com/advisories/GHSA-qr94-6q3v-pgvj)

## Where the pattern is likely to recur

- **High audit priority** for Perl identity services and administrative portals that deploy Strong::Random. Confirm the deployed version and trace the dependency to specific issuance paths. A dependency match alone leaves token exposure unverified.
- **Medium confidence as an audit target** for identity gateways and self-service portals that maintain custom reset, invitation, or recovery modules. Inspect JavaScript `Math.random()`, Python `random`, PHP `mt_rand()`, and other general-purpose generators where their output feeds a bearer secret. The historical cases give a reason to prioritize these components. Exposure in any additional product remains unknown.
- **Lower confidence as an audit target** for support tools, onboarding jobs, and plugins that issue one-time links outside the main authentication service. These components can retain independent token helpers after the primary application adopts a secure provider. Verify the issuing service and its deployed generator before assigning risk.

The pattern can recur when developers reuse a convenient random helper, copy a legacy token utility, or add a second issuance path outside the shared identity service. Functional tests can pass when generated values are distinct even though they are predictable. Review the source of the randomness as part of testing each issuance path.

## Early signals to watch

- Track oss-security follow-ups and MetaCPAN release notes for Strong::Random. Confirm which deployed versions and call sites are affected if maintainers clarify the scope or publish a fix.
- Review ZDI upcoming listings and vendor advisories for account recovery and token issuance reports. Watch release notes and public changes for quiet switches to cryptographic randomness, removal of time-derived seeds, or changes to token generation. Treat sparse descriptions as leads for internal review until the vendor provides enough detail to establish exposure.
- Apply the same review to researcher talks and maintainer discussions that flag custom recovery flows or token helpers. Ask which services in your estate implement the same design before a product or CVE is named.

## Prepare now

1. Inventory services and background jobs that issue bearer secrets. Record each owner, deployed dependency version, generator, token scope, lifetime, and revocation capability. Start with externally reachable account recovery and administrative access.
2. Route generation through the platform's cryptographic randomness API. Review callers that supply seeds or derive tokens from timestamps, identifiers, or counters. Verify single-use redemption and short lifetimes where the workflow permits them.
3. Restrict reachability of administrative recovery endpoints and isolate token issuers from unrelated services. Apply per-account and per-source redemption limits tuned to normal traffic. Prepare a way to revoke outstanding tokens and revoke affected tokens if the review confirms exposure.
4. Use the Sigma correlation and Kusto hunts to review duplicate issuance and unusual redemption activity. Keep bearer tokens and reset URLs out of logs. Predictable generators can issue unique values, so trace generation paths even when the hunts return no matches.
