#!/usr/bin/env python3
"""Inventory local nginx package, socket, and HTTP/2 configuration evidence."""

from pathlib import Path
import re
import shlex
import shutil
import subprocess

from mitigate import disable_http2


DEBIAN_FLOORS = {
    '12': ('1.22.1-9+deb12u11', 'reported by the distribution tracker; confirm DLA-4918-1'),
    '13': ('1.26.3-3+deb13u11', 'reported in the oss-sec update'),
}


def run(*args):
    if not shutil.which(args[0]):
        return None
    return subprocess.run(args, capture_output=True, text=True, check=False)


def main():
    release = {}
    for line in Path('/etc/os-release').read_text().splitlines():
        key, separator, value = line.partition('=')
        if separator and key in {'ID', 'VERSION_ID'}:
            release[key] = shlex.split(value)[0] if value else ''
    print('Distribution:', release.get('ID', '?'), release.get('VERSION_ID', '?'))

    nginx = shutil.which('nginx')
    owner = run('dpkg-query', '-S', nginx) if nginx else None
    binary_package = None
    if owner and owner.returncode == 0:
        match = re.fullmatch(r'([^,\n]+): /[^\n]+\n?', owner.stdout)
        if match:
            binary_package = match[1]
    packages = run('dpkg-query', '-W', '-f=${db:Status-Abbrev}\t${binary:Package}\t${source:Package}\t${source:Version}\n', 'nginx*')
    fixed = False
    below = False
    floor = DEBIAN_FLOORS.get(release.get('VERSION_ID')) if release.get('ID') == 'debian' else None
    if packages:
        for line in packages.stdout.splitlines():
            fields = line.split('\t')
            if len(fields) != 4 or not fields[0].startswith('ii'):
                continue
            _, package, source, version = fields
            print(f'Installed: {package} (source {source} {version})')
            if floor and binary_package and package.split(':')[0] == binary_package.split(':')[0] and source == 'nginx':
                print(f'Debian comparison floor: {floor[0]} ({floor[1]})')
                result = run('dpkg', '--compare-versions', version, 'ge', floor[0])
                fixed = bool(result and result.returncode == 0)
                below = bool(result and result.returncode == 1)
    rpm_owner = run('rpm', '-qf', nginx) if nginx else None
    if rpm_owner and rpm_owner.returncode == 0:
        print('RPM owner:', rpm_owner.stdout.strip())
    if nginx:
        version = run(nginx, '-v')
        if version and version.returncode == 0:
            print('Binary:', version.stderr.strip() or version.stdout.strip())
    else:
        print('nginx binary unavailable via PATH.')
    if not fixed and not below:
        print('Package coverage unknown. Match package provenance, release and stream to advisories covering both CVEs. Reported upstream fixed builds are 1.30.7 and 1.31.9. Distribution packages may carry backports.')

    sockets = run('ss', '-H', '-ltnp')
    if sockets and sockets.returncode == 0:
        print('Local TCP listening sockets (process attribution depends on privileges):')
        for row in sockets.stdout.splitlines():
            print(' ', row)
        if not sockets.stdout.strip():
            print('  None visible in this network namespace.')
    else:
        print('Local TCP socket inventory unavailable.')

    root = Path('/etc/nginx')
    hits = []
    try:
        paths = sorted({root / 'nginx.conf', *root.rglob('*.conf'), *(root / 'sites-enabled').glob('*')}) if root.is_dir() else []
        for path in paths:
            if path.is_file() and path.relative_to(root).parts[0] != 'sites-available':
                config = path.read_text(encoding='utf-8')
                if disable_http2(config) != config:
                    hits.append(path)
                    print('HTTP/2 enabling directive found in:', path)
                    if re.search(r'(?m)^\s*proxy_pass\s', config):
                        print('  Also contains proxy_pass. Verify both directives apply to the same listener.')
    except (OSError, UnicodeError) as error:
        print('Configuration inventory incomplete:', error)
    if not hits:
        print('No HTTP/2 enabling directive observed in readable files inspected.')
    print('Verify active includes, running binary, container namespaces and public ingress against inventory. Local sockets alone cannot establish public reachability.')
    if below:
        print('VERDICT: Below reported Debian fix floor.' + (' HTTP/2 configuration evidence found. Prioritize ingress and active-config verification.' if hits else ' Confirm whether the running service accepts HTTP/2.'))
    elif fixed:
        print('VERDICT: Installed Debian binary package meets the reported fix floor. Confirm advisory coverage, package origin and that workers run the updated binary.')
    else:
        print('VERDICT: Exposure undetermined from local evidence.')


if __name__ == '__main__':
    main()
