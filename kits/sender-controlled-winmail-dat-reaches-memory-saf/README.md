# Sender-controlled TNEF in libytnef

Prioritize mail systems that automatically pass incoming attachments to libytnef, including `ytnefprocess` procmail recipes and mail-to-calendar workers. The supplied advisory summary describes out-of-bounds reads, a heap overflow write, and a null-pointer dereference. Upstream lists releases through 2.1.2 as affected and 2.1.3 as fixed. Confirm that a distribution backport covers the upstream advisory and both reported CVEs before relying on it. Public PoCs, code execution, and exploitation in the wild remain unconfirmed in the supplied material. [Upstream advisory](https://github.com/Yeraze/ytnef/security/advisories/GHSA-jhg4-xcxm-cfg6) · [Release notes](https://github.com/Yeraze/ytnef/releases/tag/v2.1.3)

## check_exposure.sh

Run `./check_exposure.sh` on each Debian-based worker. It inventories installed packages, parser commands on PATH, common configuration locations, and local TCP mail listeners. Exit 1 calls for review. Trace handlers to the parser binary and library they actually load. Check container images, custom worker definitions, and inaccessible account recipes separately.

## mitigate.sh

Preview with `./mitigate.sh --stop-unit your-decoder.service`. Once you verify the unit only handles TNEF and confirm the upstream queue retains its work, use `./mitigate.sh --apply --stop-unit your-decoder.service` with appropriate systemd permissions. The runtime mask lasts until reboot or manual removal. For procmail, edit the site-specific recipe to bypass automatic decoding and verify delivery to the chosen quarantine or queue with a benign message. Deploy 2.1.3 or a verified backport before restoring decoding.

## detection/sigma/ytnef_heap_overflow.yml

Import into your Sigma pipeline and map `Message` to the Linux log field holding the original event text. It looks for memory-safety diagnostics mentioning ytnef in the same event. Diagnostic coverage depends on the worker build and logging.

## detection/sigma/ytnef_oob_read.yml

Use the same log mapping. This rule looks for abnormal exit signals mentioning ytnef. Correlate matches with attachment delivery and worker metadata.

## detection/yara/tnef_attachment.yar

Run `yara detection/yara/tnef_attachment.yar <decoded-attachment-or-authorized-parser-dump>`. The file rule checks for TNEF magic at offset zero. The memory rule searches anywhere and can match coincidental bytes. Treat both as triage signals. Handle parser dumps as sensitive data.

## detection/network/tnef_attachment.rules

Load the Suricata rule on a sensor with visibility into plaintext SMTP on the inbound mail path. It alerts on the filename exposed by SMTP MIME decoding. Encrypted traffic and renamed attachments can evade filename visibility. Benign TNEF can match.

## hunt.md

Use the Splunk, Defender XDR, or local log queries to find deliveries and worker faults. Review message or queue IDs where available before escalating a correlated event.

## Prepare now

Verify safe queueing before pausing automatic decoders. Review other sender-controlled attachment parsers for the same exposure and isolate those workers from mailbox credentials and writable mail stores.
