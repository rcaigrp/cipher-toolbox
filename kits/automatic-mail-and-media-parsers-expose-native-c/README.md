# Mail and media parser defense kit

Untrusted mail and attachments reach MIME parsers, previewers, thumbnailers and media indexers. Inventory which handlers are enabled and when they run. Resource exhaustion in the MIME parser and Mailpit is separate from the ImageIO out-of-bounds write. The Mailpit advisory describes a thumbnail request after storage. Automatic triggering on receipt remains unconfirmed. The ImageIO delivery path is unknown. [MIME parser advisory](https://github.com/zbateson/mail-mime-parser/security/advisories/GHSA-f6v3-2qmr-vfjx) · [Mailpit advisory](https://github.com/advisories/GHSA-75mr-qw9x-3r39) · [Apple advisory](https://support.apple.com/en-us/124927)

## Who is exposed

- `zbateson/mail-mime-parser` versions `>=2.0.0,<3.0.6` and `>=4.0.0,<4.0.2`. Update to `3.0.6` or `4.0.2` on the applicable branch.
- Mailpit through `1.30.3`. Update to `1.30.4` or later.
- Apple shipped the ImageIO fix in macOS Sequoia `15.6.1`. Verify Apple deployments separately from the Debian checks below.

## `check_exposure.py`

Run `python3 check_exposure.py --project /path/to/composer-project --unit parser-worker.service`. Repeat either option to cover additional projects or units. It reads local Composer installed metadata, the Mailpit version on PATH, systemd service settings and candidate Mailpit listen sockets in the current network namespace. Exit codes are `0` for no finding in scope, `1` for an affected version and `2` for unresolved coverage or settings to review. Inventory container images, alternate binaries, nonstandard listeners and application-level parser budgets separately.

## `mitigate.sh`

Run `bash mitigate.sh parser-worker.service 100 512 32` to preview an example drop-in for a dedicated systemd worker with no IP networking requirements. Set limits from measured workload. Explicit `--apply` before the unit installs the drop-in for an existing non-root worker. Review inherited sockets, Unix-socket proxies and drop-in precedence before reloading systemd and restarting the worker. Removing the drop-in, reloading and restarting reverts the service change. Enforce per-message CPU time, parser concurrency, MIME depth, header and decoded-pixel limits in the application.

## `detection/sigma_mail_parser.yml`

Map your parser and resource-exhaustion telemetry to the rule fields before enabling it. Correlate matches with worker CPU, memory, OOM events and request volume.

## `detection/yara_mail_parser.yar`

Use `yara detection/yara_mail_parser.yar /path/to/local-artifact` for diagnostic artifact triage. The strings are generic resource-pressure markers and can occur in ordinary logs or binaries. A match gives no evidence that an attachment is malicious.

## `detection/mailpit_thumbnail.rules`

Set `MAILPIT_SERVERS` and `MAILPIT_HTTP_PORTS` in Suricata and replace the placeholder with a path marker observed in legitimate local thumbnail traffic. Use a sensor that can see HTTP after TLS termination. Compare alerts with baseline request rates and resource telemetry. The burst threshold can miss a single expensive request.

## `hunt.md`

Adapt the SPL, KQL and grep/jq examples to your log schema, time units and expected workload. Review resource pressure around MIME parse work and thumbnail requests.

## Prepare now

Map each untrusted-input handler to its worker, patch owner, trigger and network dependencies. Apply default-deny egress and resource limits to dedicated workers and verify effective settings before enabling more preview or indexing paths.
