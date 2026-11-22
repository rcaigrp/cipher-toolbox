# Hunts for document conversion workers

The Sigma rule expects Linux process creation telemetry with resolved executable paths in `Image` and `ParentImage`. Test the mapping with an ordinary conversion job and a benign shell child in an isolated test worker. Verify that a normal renderer invocation without a matching child produces no alert. Scope production hunts to dedicated worker identities or cgroups.

The following pseudocode queries assume normalized process, network, and file telemetry. Join events by host and stable process entity ID or by cgroup and job ID. Include descendants when the backend supports ancestry.

```text
PROCESS_EVENTS
| where worker_role == 'document-conversion'
| where renderer_ancestor == true
| where executable_path not in approved_executables_for_worker_image
| display time, host, job_id, image_digest, parent_path, executable_path

NETWORK_EVENTS
| where worker_role == 'document-conversion'
| where direction == 'outbound'
| where destination not in approved_destinations_for_worker_image
| display time, host, job_id, process_entity_id, destination, disposition

FILE_EVENTS
| where worker_role == 'document-conversion'
| where operation in ('open_read', 'open_write', 'create', 'rename')
| where path matches monitored_secret_paths
| display time, host, job_id, process_entity_id, path, disposition
```

For offline workers, use an empty destination allowlist. Include denied events when available. Set monitored paths to the deployment's actual secret mounts and service credential locations. Correlate findings with the job and image digest so ordinary delegate behavior can be attributed to a known configuration. In-process file or network activity can occur without a child process, so collect those events independently. Encrypted traffic and document bytes alone provide limited evidence of these runtime behaviors.
