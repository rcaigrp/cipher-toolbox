#!/usr/bin/env python3
"""Disable client HTTP/2 in explicitly selected nginx configuration files."""

import argparse
import difflib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

# Keep quoted strings and comments intact. Split directives at structural tokens.
TOKEN = re.compile(r'''\#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\\.|[^\s;{}#"'\\]+|[;{}]''')


def disable_http2(config):
    directive = []
    edits = []
    for token in TOKEN.finditer(config):
        value = token.group()
        if value.startswith('#'):
            continue
        if value in ('{', '}', ';'):
            if value == ';' and directive:
                words = [item.group() for item in directive]
                if words == ['http2', 'on']:
                    edits.append((*directive[1].span(), 'off'))
                elif words[0] == 'listen':
                    for option in directive[2:]:
                        if option.group() == 'http2':
                            edits.append((*option.span(), ''))
            directive.clear()
        else:
            directive.append(token)
    for start, end, replacement in reversed(edits):
        config = config[:start] + replacement + config[end:]
    return config


def stage(path, content, metadata):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.nginx-http2-', delete=False) as output:
        temporary = Path(output.name)
        try:
            os.fchown(output.fileno(), metadata.st_uid, metadata.st_gid)
            os.fchmod(output.fileno(), metadata.st_mode & 0o7777)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    return temporary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', type=Path, help='Files containing the directives for the affected listeners')
    parser.add_argument('--apply', action='store_true', help='Write changes and validate the default nginx configuration')
    args = parser.parse_args()
    if not args.files:
        if args.apply:
            parser.error('--apply requires explicit configuration paths')
        print('DRY RUN: select the files defining the affected listeners. The plan changes http2 on to http2 off and removes the legacy http2 listen option. No files selected.')
        return
    candidates = {}
    for supplied in args.files:
        path = supplied.resolve(strict=True)
        info = path.stat()
        if not path.is_file() or info.st_nlink != 1:
            parser.error(f'expected a regular configuration file with one hard link: {path}')
        before = path.read_bytes()
        original = before.decode('utf-8')
        revised = disable_http2(original)
        if original != revised and path not in candidates:
            candidates[path] = (before, revised.encode('utf-8'), info)
            print(''.join(difflib.unified_diff(original.splitlines(True), revised.splitlines(True), fromfile=str(path), tofile=str(path) + ' (proposed)')), end='')
    if not candidates:
        print('No supported HTTP/2 enabling directives found in the selected files.')
        return
    if not args.apply:
        print('\nDRY RUN: no files changed. Apply validates the default nginx configuration and leaves reload to the operator.')
        return
    nginx = shutil.which('nginx')
    if not nginx:
        parser.error('nginx is required to validate changes')
    subprocess.run([nginx, '-t'], check=True)
    originals = {}
    staged = {}
    installed = []
    try:
        for path, (before, after, info) in candidates.items():
            originals[path] = stage(path, before, info)
            staged[path] = stage(path, after, info)
        for path, (before, _, info) in candidates.items():
            current = path.stat()
            if (current.st_dev, current.st_ino, current.st_mtime_ns) != (info.st_dev, info.st_ino, info.st_mtime_ns) or path.read_bytes() != before:
                raise RuntimeError(f'configuration changed during planning: {path}')
            os.replace(staged[path], path)
            installed.append(path)
        subprocess.run([nginx, '-t'], check=True)
    except BaseException:
        for path in reversed(installed):
            backup = originals.pop(path)
            try:
                os.replace(backup, path)
            except OSError as error:
                print(f'Restore failed for {path}. Original saved at {backup}: {error}', flush=True)
        raise
    finally:
        for temporary in (*originals.values(), *staged.values()):
            temporary.unlink(missing_ok=True)
    print('\nConfiguration updated and nginx -t passed. Reload the intended nginx instance to activate changes.')


if __name__ == '__main__':
    main()
