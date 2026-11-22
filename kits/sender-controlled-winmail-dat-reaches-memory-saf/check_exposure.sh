#!/usr/bin/env bash
set -euo pipefail

packages=$(dpkg-query -W -f='${db:Status-Status}\t${binary:Package}\t${Version}\n')
review=0
found=0
while IFS=$'\t' read -r status package version; do
    [[ $status == installed && $package =~ ^(libytnef[[:alnum:].+-]*|ytnef|ytnef-tools)(:[[:alnum:]-]+)?$ ]] || continue
    found=1
    upstream=${version#*:}
    upstream=${upstream%-*}
    if [[ $upstream =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] && dpkg --compare-versions "$upstream" ge 2.1.3; then
        printf '%s %s: meets upstream version floor; confirm running worker uses this build\n' "$package" "$version"
    else
        printf '%s %s: patch status requires review; verify vendor backport coverage\n' "$package" "$version"
        review=1
    fi
done <<< "$packages"
(( found )) || printf 'No installed Debian TNEF packages matched.\n'

printf '\nTNEF executables on PATH:\n'
for executable in ytnef ytnefprocess; do
    if path=$(command -v "$executable"); then
        printf '%s\n' "$path"
        if ! dpkg-query -S "$path" >/dev/null 2>&1; then
            printf 'Package ownership unknown; verify this executable and its linked library.\n'
            review=1
        fi
    fi
done

printf '\nAutomatic processing config references:\n'
shopt -s nullglob
for config in /etc/procmailrc /etc/procmailrcs /etc/postfix /etc/exim4 /etc/dovecot /etc/mail /etc/systemd/system /etc/cron.d "$HOME/.procmailrc" /home/*/.procmailrc; do
    [[ -e $config ]] || continue
    if grep -EriIn -- 'ytnef|winmail\.dat|application/(ms-tnef|vnd\.ms-tnef)' "$config"; then
        review=1
    else
        result=$?
        if (( result != 1 )); then
            printf 'Could not fully inspect %s\n' "$config"
            review=1
        fi
    fi
done

printf '\nLocal TCP listeners on common mail ports (listener presence alone does not establish TNEF exposure):\n'
if command -v ss >/dev/null && listeners=$(ss -H -ltnp); then
    awk '$4 ~ /:(24|25|110|143|465|587|993|995|4190)$/ {print}' <<< "$listeners"
else
    printf 'Local listener inventory unavailable.\n'
    review=1
fi

if (( review )); then
    printf '\nVERDICT: REVIEW REQUIRED. Trace configured handlers to their loaded parser and verify the fix.\n'
    exit 1
fi
printf '\nVERDICT: No unresolved TNEF indicators in checked locations. Check custom workers, containers and uninspected mailboxes separately.\n'
