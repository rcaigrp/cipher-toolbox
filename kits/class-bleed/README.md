# Out-of-bounds reads in untrusted-input parsers

Read [FORESIGHT.md](FORESIGHT.md) for the advisory evidence, review targets and containment priorities. Run `python3 check_exposure.py` for a read-only inventory of selected Debian packages and tools on PATH. Check worker configuration, containers and embedded copies separately.

## Detection deployment

- **Sigma** expects trusted worker telemetry tagged with `ServiceRole=untrusted_input_parser`. Configure `Message` to contain one complete AddressSanitizer report per event, with the error header and access type together. Adapt the log source and fields in your backend.
- **YARA** scans individual diagnostic reports from trusted worker stderr. Route the scan through known worker identity and avoid running it on raw user uploads or mixed log archives.
- **Splunk hunt** groups abnormal exits of automatic parsing jobs by service, format and 15-minute interval. Map the index, source type and fields to your environment. Tune the starting threshold of three distinct crashed jobs against baseline data. Correlate with deployment changes and sanitizer diagnostics before escalating.

Sanitizer rules require instrumented builds with diagnostics enabled. A crash cluster is a triage signal. Silent overreads require other visibility, such as instrumented regression runs and review of response boundaries.

Validate using synthetic log text. A trusted parser worker report containing `ERROR: AddressSanitizer: heap-buffer-overflow` and `READ of size 4` should match both diagnostic rules. A report with `WRITE of size 4` should miss both. For the hunt, three distinct job IDs with the same service and format inside one interval should surface, while repeated log records for a single job should stay below threshold.
