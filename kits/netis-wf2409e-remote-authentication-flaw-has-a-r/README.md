# Netis WF2409E management exposure kit

The exposure checks inventory local TCP listeners on ports 80, 443, 8080, and 8443. They make no network requests. Review router identity, hardware revision, firmware, WAN management, upstream forwarding, and internet reachability using existing inventory and configuration records. The supplied material identifies no verified fixed firmware release.

## Usage

Run from this directory. The checks require `ss` from `iproute2`.

```bash
bash check_exposure.sh
python3 check_exposure.py
bash mitigate.sh
```

`mitigate.sh` prints a dry-run isolation plan covering WAN management, forwarding, and approved management networks. `--apply` exits with status 2 without changing configuration because the kit has no verified device-specific procedure.

## Detection and hunting

- `hunt.md` contains a firewall log query and sample-event validation guidance.
- `detection/netis-wf2409e-management.rules` flags connection attempts to inventoried management endpoints from outside approved networks.
- `detection/sigma/netis-wf2409e-auth-flaw.yml` provides a firewall log template. Substitute your inventory, allowlist, and field mappings before deployment.
- `detection/yara/netis-wf2409e-exploit.yar` is included for review. Validate its indicators against confirmed incident evidence before relying on it.

## Tests

```bash
python3 -m pytest test/test_kit.py -v
```

The suite uses synthetic local listener output and checks the mitigation script's dry-run and `--apply` behavior.
