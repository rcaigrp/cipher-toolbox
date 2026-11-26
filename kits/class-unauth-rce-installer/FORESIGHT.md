# Public exposure of web application setup workflows

Setup workflows can create privileged accounts, write configuration, or initialize a datastore before ordinary application authentication is available. The class is a failure to restrict who can enter that workflow or when it can run. The impact depends on the privileges the workflow confers. The feed reports active exploitation of a Drupal installer issue under CVE-2026-132165 and separately mentions an installer patch gap. The supplied material does not establish affected releases, the exact mechanism, or whether the patch-gap headline describes the same issue.

## Historical precedent and variant review

Atlassian identifies CVE-2023-22515 as a critical authentication vulnerability in Confluence Server and Data Center. It is a precedent for reviewing bootstrap authorization and monitoring unexpected administrator creation. [Atlassian FAQ](https://support.atlassian.com/atlassian-knowledge-base/kb/faq-for-cve-2023-22515/)

- **Drupal and downstream deployment templates — high priority for inventory.** Review deployments that ship the web installer, including staging copies and restored snapshots. Confirm whether setup is restricted before the first public request. Confidence is high that the installer is relevant to the reported issue, while specific version and deployment applicability remain unverified.
- **Jenkins controller provisioning — medium-priority design review.** Jenkins documents a post-installation wizard. Review when a new instance is created or restored, especially if it shares setup code with an internet-facing controller. A default virtual host or alternate ingress can bypass restrictions applied only to the main hostname. The installer is often part of the base image, so this could be a high-priority concern for any Jenkins deployment that allows direct backend access.
- **Other web apps with setup wizards — medium priority.** Any application that uses a web-based setup workflow, such as TastyIgniter or other CMS platforms, should be reviewed. The pattern is likely to appear in any application that allows an unauthenticated path to create privileged users or execute arbitrary code.

## Why exposure can recur

Initial deployment, restore, and replica replacement can publish an endpoint before initialization completes. A default virtual host or alternate ingress can also bypass a restriction applied only on the main hostname. Review setup authorization across fresh, initialized, and restored instances, including direct backend access and every ingress policy.

## Early warning

Review vendor release notes and public security mailing lists for changes to installer access, first-run administrator creation, setup completion checks, restore behavior, or default ingress rules. Treat a report that an initialized instance has unexpectedly offered setup as an internal investigation trigger. The ZDI page checked during this session returned 404, so upcoming disclosure coverage remains unverified.

## Prepare now

Inventory web installers with their owning team, authorized provisioning network, setup routes and hostnames, and expected provisioning windows. Keep setup behind private or authenticated management access before the service is published and deny it at ingress after provisioning where supported. Apply the policy to alternate hostnames and direct backend routes. Log setup requests, administrator creation and grants, configuration writes, and web-worker process starts. Prioritize investigations where setup activity outside a provisioning window coincides with a privileged state change on the same instance.

See [HUNTS.md](HUNTS.md) for log fields, correlation guidance, and synthetic validation. The local exposure check inventories installer artifacts. Use it alongside ingress and application configuration review to establish reachability.