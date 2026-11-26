#!/usr/bin/env bash
# Inventory template compilation sites for manual review.
set -u

usage() {
    printf 'Usage: %s SOURCE_DIRECTORY\n' "${0##*/}"
    printf 'List local source files that may compile templates at runtime.\n'
    printf 'Review whether each call receives template text from an untrusted source.\n'
}

if [[ $# -eq 1 && ( $1 == --help || $1 == -h ) ]]; then
    usage
    exit 0
fi
if [[ $# -ne 1 || ! -d $1 ]]; then
    usage >&2
    exit 2
fi

pattern='(^|[^[:alnum:]_])(render_template_string|from_string|createTemplate|Handlebars[[:space:]]*\.[[:space:]]*compile|Environment[[:space:]]*\.[[:space:]]*from_string)[[:space:]]*\('
LC_ALL=C grep -rIlE --include='*.py' --include='*.php' --include='*.js' --include='*.ts' --include='*.mjs' --include='*.cjs' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=vendor -- "$pattern" "$1"
status=$?
case $status in
    0) printf 'Review the listed files for untrusted input reaching template compilation.\n' >&2 ;;
    1) printf 'No supported template compilation calls found.\n' >&2 ;;
    *) printf 'Source inventory failed or was incomplete.\n' >&2; exit 2 ;;
esac
