#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 test.py
python3 - <<'TEST_PY'
import contextlib
import io
import json
from unittest.mock import patch

import detect_jailbreak as detector

with open('test_input.json', encoding='utf-8') as fixture_file:
    fixtures = json.load(fixture_file)

with patch.object(detector, 'USE_LLM', False):
    for group, expected in (('benign', False), ('malicious', True)):
        for index, prompt in enumerate(fixtures[group]):
            with patch.object(detector.sys, 'argv', ['detect_jailbreak.py', '--input', prompt]):
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    detector.main()
            assert json.loads(stdout.getvalue())['is_jailbreak'] is expected, (group, index)

with patch.object(detector.requests, 'post') as post:
    response = post.return_value
    response.status_code = 200
    for content, expected in (('safe', 'safe'), ('unsafe', 'unsafe'), ('invalid', 'unknown')):
        response.json.return_value = {'choices': [{'message': {'content': content}}]}
        assert detector.classify_with_llm('A sample prompt') == expected
    assert post.call_args.args[0] == detector.LLM_URL + '/chat/completions'
    post.side_effect = detector.requests.ConnectionError('simulated connection failure')
    with contextlib.redirect_stderr(io.StringIO()) as stderr:
        assert detector.classify_with_llm('A sample prompt') == 'unknown'
    assert stderr.getvalue()

print('Fixture and mocked classifier checks passed')
TEST_PY
