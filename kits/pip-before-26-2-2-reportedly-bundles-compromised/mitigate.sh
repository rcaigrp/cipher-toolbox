#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bash mitigate.sh [--apply] [--python PATH --wheel FILE --sha256 TRUSTED_HASH]"
    echo "Use a locally staged pip wheel and obtain its pinned SHA-256 from an independently trusted source."
}

apply=0
python_bin=python3
wheel=''
sha256=''
while (($#)); do
    case "$1" in
        --apply) apply=1; shift ;;
        --python|--wheel|--sha256)
            if (($# < 2)) || [[ "$2" == --* ]]; then usage >&2; exit 2; fi
            case "$1" in
                --python) python_bin=$2 ;;
                --wheel) wheel=$2 ;;
                --sha256) sha256=$2 ;;
            esac
            shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done

if (( ! apply )); then
    printf 'Dry run. Would use %q to install pip 26.2.2 or later from a hash-pinned local wheel with indexes and dependencies disabled.\n' "$python_bin"
    printf 'Wheel: %s\n' "${wheel:-required for --apply}"
    echo 'Would verify the installed version with the same interpreter.'
fi

if [[ -z "$wheel" && -z "$sha256" ]] && (( ! apply )); then exit 0; fi
if [[ ! -f "$wheel" || ! "$sha256" =~ ^[0-9a-fA-F]{64}$ ]]; then
    usage >&2
    exit 2
fi

"$python_bin" -I -B - "$apply" "$wheel" "$sha256" <<'PY'
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from pip._vendor.packaging.utils import parse_wheel_filename
from pip._vendor.packaging.version import Version

apply, wheel_arg, expected = sys.argv[1:]
wheel = Path(wheel_arg)
fixed = Version('26.2.2')
name, version, _, _ = parse_wheel_filename(wheel.name)
if name != 'pip' or version < fixed or version.is_prerelease:
    sys.exit('Supply a stable pip wheel at version 26.2.2 or later.')


def verify(path):
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else digest_stream(stream)
    if actual != expected.lower():
        sys.exit('Wheel SHA-256 does not match the trusted pin.')


def digest_stream(stream):
    digest = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        digest.update(block)
    return digest.hexdigest()


verify(wheel)
if apply == '0':
    print(f'Verified staged pip {version} wheel against the supplied pin.')
    sys.exit(0)

env = {key: value for key, value in os.environ.items() if not key.startswith('PIP_')}
env['PIP_CONFIG_FILE'] = os.devnull
python = [sys.executable, '-I', '-B']
with tempfile.TemporaryDirectory(prefix='pip-remediation-') as directory:
    staged = Path(directory) / wheel.name
    shutil.copyfile(wheel, staged)
    verify(staged)
    requirements = Path(directory) / 'requirements.txt'
    requirements.write_text(f'pip @ {staged.as_uri()} --hash=sha256:{expected.lower()}\n', encoding='utf-8')
    subprocess.run(python + ['-m', 'pip', '--disable-pip-version-check', 'install', '--no-index', '--no-deps', '--no-cache-dir', '--require-hashes', '--upgrade', '--force-reinstall', '-r', str(requirements)], env=env, check=True)

subprocess.run(python + ['-c', "import pip; from pip._vendor.packaging.version import Version; v = Version(pip.__version__); assert v >= Version('26.2.2') and not v.is_prerelease, v; print(f'Verified pip {v}')"], env=env, check=True)
PY
