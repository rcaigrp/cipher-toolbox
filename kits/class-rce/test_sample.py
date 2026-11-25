import subprocess
import sys
from pathlib import Path


def test_scan_sample(tmp_path):
    flagged = tmp_path / 'flagged.py'
    flagged.write_text('# Sample eval(sample_expression)\n', encoding='utf-8')
    clean = tmp_path / 'clean.py'
    clean.write_text('# Sample print(sample_expression)\n', encoding='utf-8')

    scanner = Path(__file__).with_name('check_exposure.py')
    result = subprocess.run(
        [sys.executable, str(scanner), str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert f'File: {flagged}' in result.stdout
    assert 'Line: 1' in result.stdout
    assert 'Match: eval(' in result.stdout
    assert f'File: {clean}' not in result.stdout
