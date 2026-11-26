#!/usr/bin/env python3
"""Inventory Python re call sites for manual exposure review without running regexes."""

import argparse
import ast
from pathlib import Path
import sys
import tokenize


PATTERN_CALLS = {'compile', 'findall', 'finditer', 'fullmatch', 'match', 'search', 'split', 'sub', 'subn'}


def inventory(path):
    with tokenize.open(path) as source:
        tree = ast.parse(source.read(), filename=str(path))

    modules = set()
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 're':
                    modules.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module == 're':
            for alias in node.names:
                if alias.name in PATTERN_CALLS:
                    functions[alias.asname or alias.name] = alias.name

    calls = sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.Call)),
        key=lambda node: (node.lineno, node.col_offset),
    )
    for call in calls:
        function = call.func
        if isinstance(function, ast.Name):
            name = functions.get(function.id)
        elif isinstance(function, ast.Attribute) and isinstance(function.value, ast.Name) and function.value.id in modules:
            name = function.attr
        else:
            continue
        if name not in PATTERN_CALLS:
            continue
        pattern = call.args[0] if call.args else next(
            (argument.value for argument in call.keywords if argument.arg == 'pattern'), None
        )
        literal = isinstance(pattern, ast.Constant) and isinstance(pattern.value, (str, bytes))
        kind = 'literal pattern' if literal else 'dynamic or unresolved pattern'
        print(f'{path}:{call.lineno}:{call.col_offset + 1}: re.{name}: {kind}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path, metavar='PYTHON_FILE')
    args = parser.parse_args()
    failed = False
    for path in args.files:
        try:
            inventory(path)
        except (OSError, SyntaxError, UnicodeError, ValueError) as error:
            print(f'{path}: {error}', file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
