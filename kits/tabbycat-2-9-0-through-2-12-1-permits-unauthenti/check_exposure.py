#!/usr/bin/env python3
"""
Tabbycat Exposure Checker

Checks if a Tabbycat deployment is exposed to CVE-2026-135429
"""

import argparse
import subprocess
import sys
import os


def get_version_from_package():
    """Get version from installed package."""
    try:
        import importlib.metadata
        for name in ('tabbycat-debate', 'tabbycat'):
            try:
                return importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                continue
    except ImportError:
        # Fallback for older Python versions
        try:
            import pkg_resources
            for name in ('tabbycat-debate', 'tabbycat'):
                try:
                    return pkg_resources.get_distribution(name).version
                except pkg_resources.DistributionNotFound:
                    continue
        except ImportError:
            pass
    return None


def check_git_repo(repo_path, fix_commit):
    """Check if git repo contains the fix."""
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'merge-base', '--is-ancestor', fix_commit, 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description='Check Tabbycat exposure to CVE-2026-135429')
    parser.add_argument('--version', help='Explicit version to check')
    parser.add_argument('--repo', help='Path to local git checkout')
    parser.add_argument('--nginx-include', help='Path to nginx include file')
    
    args = parser.parse_args()
    
    # Get version
    if args.version:
        version = args.version
    else:
        version = get_version_from_package()
    
    print(f'Reported version: {version or "unknown"}')
    
    # Check fix presence
    fix = 'b7f0746ba9cb5a23f94ac169dbe5b68a5fbd1ab2'
    print(f'Known upstream fix: {fix}. Fixed tagged release unconfirmed.')
    
    fix_present = False
    if args.repo and os.path.exists(args.repo):
        fix_present = check_git_repo(args.repo, fix)
        print(f'Fix present in repo: {fix_present}')
    
    # Check nginx guard
    if args.nginx_include:
        if os.path.exists(args.nginx_include):
            print(f'Nginx guard file exists: {args.nginx_include}')
        else:
            print(f'Nginx guard file missing: {args.nginx_include}')
    
    # Determine exposure
    if version:
        # Check if version is vulnerable (2.9.0 through 2.12.1)
        try:
            from packaging import version as pkg_version
            parsed_version = pkg_version.parse(version)
            if pkg_version.parse('2.9.0') <= parsed_version <= pkg_version.parse('2.12.1'):
                vulnerable = True
            else:
                vulnerable = False
        except ImportError:
            # Fallback - simple string comparison
            if version >= '2.9.0' and version <= '2.12.1':
                vulnerable = True
            else:
                vulnerable = False
    else:
        vulnerable = None
    
    print(f'Version vulnerable: {vulnerable}')
    
    # Final assessment
    if vulnerable is True:
        print('EXPOSURE: This deployment may be vulnerable to CVE-2026-135429')
        return 1
    elif vulnerable is False:
        print('NO EXPOSURE: This deployment is not vulnerable to CVE-2026-135429')
        return 0
    else:
        print('UNKNOWN: Unable to determine vulnerability status')
        return 2


if __name__ == '__main__':
    sys.exit(main())