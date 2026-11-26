# Regular expression denial of service

## Pattern

A regex operation can consume disproportionate CPU when a backtracking engine explores many possible matches against externally supplied text. Growth can be polynomial or exponential. The operational impact depends on input size, evaluation limits, concurrency, and whether matching blocks shared request workers or a job queue. The feed’s PDF::API2 recursion and SkyWalking BanyanDB query-limit items share the broader pattern of unbounded work on external input. Their headlines describe different mechanisms from ReDoS.

## Precedents and adjacent exposure

- **npm semver, CVE-2022-25883.** A semantic-version parser had a ReDoS issue. Review dependency metadata processors, package registries, and CI gates that parse contributor-controlled version ranges. Confidence is high that these are relevant review targets. Exposure depends on the installed dependency and input path. [Research disclosure](https://security.snyk.io/vuln/SNYK-JS-SEMVER-3247795)
- **chalk/ansi-regex, CVE-2021-3807.** The maintainer documented a fix in v6.0.1 and identified server-side use on untrusted input as the relevant context. Review hosted CI log viewers, terminal-output sanitizers, and ingestion workers that reuse ANSI stripping code. Confidence is high for the design analogy and unknown for any specific deployment. [Maintainer release](https://github.com/chalk/ansi-regex/releases/tag/v6.0.1)
- **Gateway and application routing.** Review regex-backed header checks, URL routing, and policy filters where external inputs reach a backtracking engine on a shared worker. Confidence is moderate because engine choice, route configuration, and upstream size limits vary.

Shared parsing and normalization libraries can move from local CLI tools into long-running services. The same operation then handles repeated external inputs and can consume a shared worker budget. Prioritize review by reachability and worker impact.

## Early warning

Watch maintainer release notes and security mailing lists for reports of slow rejection, parser CPU spikes, tighter maximum lengths, regex engine substitutions, and new match limits. Track upcoming disclosures when public summaries identify an input-processing or availability issue. Treat terse performance fixes as leads for review. The supplied feed does not establish a new ReDoS case or a current pre-disclosure match.

## Prepare now

1. Inventory external fields reaching regex evaluation, including logs and queue payloads. Record the engine, input owner, size ceiling, match budget, and worker isolation for each path.
2. Enforce byte limits before matching. Prefer bounded matching or a linear-time engine where compatible. For workloads that need backtracking features, configure engine limits or run evaluation in a worker that can be terminated. A request deadline alone may leave matching work running.
3. Isolate externally driven normalization and parsing queues with per-tenant concurrency limits and worker CPU budgets. Keep health checks and administrative controls responsive during saturation.
4. Emit regex limit events with the normalized fields in `detection.yml`. Correlate by service, route, and pattern ID with worker CPU, queue delay, and request errors. Use input size and evaluation time for triage. Keep raw input out of telemetry.

## Hunt queries

These Splunk examples assume application instrumentation and the field mapping in `detection.yml`. Replace the index name and calibrate the thresholds to the service.

```spl
index=app event_action=regex_evaluation input_origin=external (event_outcome=timeout OR event_outcome=work_limit_exceeded)
| bin _time span=5m
| stats count dc(request_id) AS requests max(input_bytes) AS largest_input max(evaluation_ms) AS slowest_match BY _time service_name route pattern_id
| sort -count
```

Where evaluations emit timing for all outcomes, compare latency by input size and outcome. A shift in the high percentiles can surface expensive evaluation before limit events appear.

```spl
index=app event_action=regex_evaluation input_origin=external evaluation_ms=* input_bytes=*
| eval size_bucket=if(input_bytes<1024,"under_1KiB",if(input_bytes<16384,"1_to_16KiB","16KiB_or_more"))
| bin _time span=15m
| stats count p95(evaluation_ms) AS p95_ms p99(evaluation_ms) AS p99_ms BY _time service_name route pattern_id size_bucket event_outcome
```
