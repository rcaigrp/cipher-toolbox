#!/usr/bin/env bash
set -euo pipefail

case "$#:${1-}" in
    0:) mode=DRY-RUN ;;
    1:--apply) mode=APPLY-BLOCKED ;;
    1:--help|-h) printf 'Usage: %s [--apply]\nPrints the mitigation plan. Apply requires deployment-specific Oracle instructions.\n' "$0"; exit 0 ;;
    *) printf 'Usage: %s [--apply]\n' "$0" >&2; exit 64 ;;
esac

printf '[%s] PeopleSoft CVE-2026-35273 and ZDI-26-1039 mitigation plan\n' "$mode"
cat <<'PLAN'
1. Record each deployment's exact PeopleTools build and installed update inventory.
2. Compare the inventory with Oracle's CVE alert and applicable November PeopleSoft updates. Ask Oracle to confirm ZDI-26-1039 coverage for the exact build.
3. Restrict management-plane access to approved administration hosts and required peers. Verify required traffic before enforcing a change.
4. Review registration privileges, peer trust, and service-account permissions. Remove access that the deployment does not require.
5. Review previously exposed instances for compromise, including those behind a WAF.

Oracle CVE alert: https://www.oracle.com/security-alerts/alert-cve-2026-35273.html
Oracle November PeopleSoft appendix: https://www.oracle.com/security-alerts/cspunov2026.html#AppendixPS
PLAN

if [[ "$mode" == APPLY-BLOCKED ]]; then
    printf '%s\n' 'No changes made. The supplied evidence does not include the Oracle installation or configuration steps needed to apply a verified fix to this deployment.' >&2
    exit 2
fi
