#!/bin/bash
set -eu

printf '%s\n' 'Local inventory of tools that may parse untrusted media or documents.'
printf '%s\n' 'Presence is an exposure lead. Review which services invoke these tools and where their inputs originate.'

for executable in MP4Box mp4box gpac ffmpeg ffprobe ytnef gs; do
    if path=$(type -P "$executable"); then
        printf 'ON PATH\t%s\t%s\n' "$executable" "$path"
    else
        printf 'NOT ON PATH\t%s\n' "$executable"
    fi
done

if type -P dpkg-query >/dev/null; then
    printf '\n%s\n' 'Matching Debian package records (installed only):'
    packages=$(dpkg-query -W -f='${db:Status-Status}\t${binary:Package}\t${Version}\n')
    printf '%s\n' "$packages" | awk -F '\t' '
        $1 == "installed" && $2 ~ /^(gpac|libgpac|ffmpeg|libavformat|libavcodec|ytnef|libytnef|ghostscript|libgs([0-9]|-))/ {
            print $2 "\t" $3
            found = 1
        }
        END { if (!found) print "No matching installed Debian packages." }
    '
else
    printf '\n%s\n' 'Debian package inventory unavailable.'
fi

printf '\n%s\n' 'Coverage is limited to the current PATH and local Debian package database. Review containers, bundled libraries, and service configurations separately.'
printf '%s\n' 'This inventory does not determine patch status or whether an untrusted input can reach a parser.'
