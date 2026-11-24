#!/usr/bin/env python3
"""Run the kit's read-only exposure checker through its Python entry point."""

import os
from pathlib import Path
import sys


def main():
    checker = Path(__file__).resolve().with_name('check_exposure.sh')
    os.execv(str(checker), [str(checker), *sys.argv[1:]])


if __name__ == '__main__':
    main()
