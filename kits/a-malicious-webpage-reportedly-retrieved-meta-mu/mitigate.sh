#!/usr/bin/env bash
set -euo pipefail

case "$#:$*" in
    '0:'|'1:--dry-run')
        printf '%s\n' 'DRY RUN: no changes.' \
            'Require trusted user approval scoped to the resource and operation before a web-enabled assistant reads chat history or saved memories.' \
            'If your gateway cannot enforce approval, remove those read permissions from browsing sessions.' \
            'Verify that missing, denied, expired or mismatched approval blocks the read. Log approval decisions and tool outcomes without storing chat or memory content.' \
            'The supplied material gives no documented Meta setting or local gateway configuration to change. These steps require manual implementation in your gateway.'
        ;;
    '1:--apply')
        printf '%s\n' 'No changes made. The supplied material gives no documented Meta setting or local gateway configuration to modify. Run in dry-run mode for the manual hardening steps.' >&2
        exit 3
        ;;
    *)
        printf '%s\n' 'Usage: mitigate.sh [--dry-run | --apply]' >&2
        exit 2
        ;;
esac
