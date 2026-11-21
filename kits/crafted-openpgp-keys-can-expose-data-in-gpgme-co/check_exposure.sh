#!/usr/bin/env bash
set -u

# Debian host inventory. No network requests and no changes to host state.
fixed=2.3.1
older=0
packages=0
incomplete=0

if ! command -v dpkg-query >/dev/null || ! command -v dpkg >/dev/null; then
    printf 'Verdict: UNKNOWN. Debian package inventory is unavailable.\n'
    exit 2
fi

printf 'Installed GPGME packages (upstream fix %s)\n' "$fixed"
while IFS=$'\t' read -r status package version; do
    [[ $status == ii* ]] || continue
    packages=$((packages + 1))
    upstream=${version#*:}
    upstream=${upstream%-*}
    if dpkg --compare-versions "$upstream" lt "$fixed"; then
        printf '  %s %s — below upstream fix; verify distributor backport for T8557\n' "$package" "$version"
        older=1
    else
        printf '  %s %s — at or above upstream fix by package version\n' "$package" "$version"
    fi
done < <(dpkg-query -W -f='${db:Status-Abbrev}\t${binary:Package}\t${Version}\n' 'libgpgme*' 'gpgme*' 2>/dev/null | awk -F '\t' '$2 ~ /^libgpgme[0-9]/ || $2 ~ /^gpgme([:-]|$)/')
(( packages > 0 )) || printf '  No matching installed runtime packages found.\n'

printf '\nGPGME libraries mapped by readable local processes\n'
for maps in /proc/[0-9]*/maps; do
    [[ -e $maps ]] || continue
    if [[ ! -r $maps ]]; then
        incomplete=1
        continue
    fi
    if ! rows=$(awk '/\/libgpgme\.so(\.|[[:space:]]|$)/ { sub(/^[^/]+/, ""); print }' "$maps" 2>/dev/null | sort -u); then
        incomplete=1
        continue
    fi
    [[ -d ${maps%/maps} ]] || continue
    [[ -n $rows ]] || continue
    pid=${maps#/proc/}
    pid=${pid%/maps}
    read -r name 2>/dev/null < "/proc/$pid/comm" || name=unknown
    while IFS= read -r library; do
        printf '  PID %s (%s) %s\n' "$pid" "$name" "$library"
        if [[ $library == *' (deleted)' ]] || ! dpkg-query -S -- "$library" >/dev/null 2>&1; then
            printf '    Verify this mapped copy; it is deleted or has no exact path match in the package database.\n'
            incomplete=1
        fi
    done <<< "$rows"
done
(( incomplete == 0 )) || printf '  Some process or library details could not be verified.\n'

printf '\nLocal TCP/UDP listeners (compare PIDs with mapped consumers)\n'
if command -v ss >/dev/null; then
    ss -lntup || incomplete=1
else
    printf '  Listener inventory unavailable: ss is missing.\n'
    incomplete=1
fi

printf '\nConfiguration review\n'
printf '  For each GPGME consumer, check whether incoming mail, uploads, queues or other unattended inputs can trigger key import or signature verification.\n'
printf '  Listener inventory cannot determine whether a service accepts untrusted OpenPGP input. Review app settings and workers even if they have no listener.\n'
if (( older )); then
    printf '\nVerdict: POTENTIALLY EXPOSED. An installed package predates 2.3.1. Confirm a distributor backport and review unattended receivers.\n'
    exit 1
fi
if (( packages == 0 || incomplete )); then
    printf '\nVerdict: UNKNOWN. Verify bundled or static copies and any inaccessible processes.\n'
    exit 2
fi
printf '\nVerdict: CHECKED PACKAGES MEET UPSTREAM VERSION FLOOR. Verify bundled or static copies and receiver configuration separately.\n'
