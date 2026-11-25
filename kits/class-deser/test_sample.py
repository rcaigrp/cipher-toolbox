import subprocess
import sys
from pathlib import Path


def test_scan_sample(tmp_path):
    flagged = tmp_path / 'flagged.py'
    flagged.write_text('# Sample: pickle.loads(sample_bytes)\n', encoding='utf-8')
    clean = tmp_path / 'clean.py'
    clean.write_text('# Sample: yaml.safe_load(sample_text)\n', encoding='utf-8')

    scanner = Path(__file__).with_name('check_exposure.py')
    result = subprocess.run(
        [sys.executable, str(scanner), str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )

    findings = [line for line in result.stdout.splitlines() if line.startswith('File: ')]
    assert findings == [f'File: {flagged}, Line: 1']
    assert r'Pattern: pickle\.loads?\s*\(' in result.stdout
