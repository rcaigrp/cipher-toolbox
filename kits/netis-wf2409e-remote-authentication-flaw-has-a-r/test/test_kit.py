import os
from pathlib import Path
import subprocess
import sys

import pytest


KIT = Path(__file__).resolve().parents[1]


def run_script(command, *args, env=None):
    return subprocess.run(
        [*command, *args], cwd=KIT, env=env, capture_output=True, text=True,
        timeout=5,
    )


@pytest.fixture(params=[(sys.executable, 'check_exposure.py'), ('./check_exposure.sh',)])
def checker(request):
    return request.param


def test_checker_help(checker):
    result = run_script(checker, '--help')
    assert result.returncode == 0, result.stderr
    assert 'Usage:' in result.stdout


@pytest.mark.parametrize(('rows', 'status', 'verdict'), [
    ('', 0, 'NO MATCHING LOCAL TCP LISTENERS'),
    ('LISTEN 0 128 127.0.0.1:80 0.0.0.0:*', 0, 'bind only to loopback'),
    ('LISTEN 0 128 0.0.0.0:443 0.0.0.0:*', 0, 'bound beyond loopback'),
    ('', 1, 'VERDICT: UNKNOWN'),
])
def test_checker_reports_listener_scope(checker, tmp_path, rows, status, verdict):
    fake_ss = tmp_path / 'ss'
    fake_ss.write_text('#!/bin/sh\nprintf "%s" "$SS_FIXTURE"\nexit "$SS_STATUS"\n')
    fake_ss.chmod(0o755)
    env = dict(os.environ, PATH=f'{tmp_path}{os.pathsep}{os.environ["PATH"]}',
               SS_FIXTURE=rows, SS_STATUS=str(status))
    result = run_script(checker, env=env)
    assert result.returncode == (2 if status else 0), result.stderr
    assert verdict in (result.stderr if status else result.stdout)


def test_mitigation_dry_run():
    result = run_script(('./mitigate.sh',))
    assert result.returncode == 0, result.stderr
    assert 'Dry run' in result.stdout
    assert 'Disable WAN management' in result.stdout


def test_mitigation_apply_declines_changes():
    result = run_script(('./mitigate.sh',), '--apply')
    assert result.returncode == 2
    assert 'No changes applied' in result.stderr
