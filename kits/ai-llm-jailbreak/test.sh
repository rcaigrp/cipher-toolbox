#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")"
exec python3 -m unittest -v test_scanner
