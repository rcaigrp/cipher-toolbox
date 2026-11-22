import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import output_guard


BENIGN = 'The maintenance window starts at nine. Save your work before then.'
SYNTHETIC_SECRET = 'Example service configuration: client_secret = DEMO_ONLY_FAKE_42'
SYNTHETIC_RECORD = 'Synthetic patient Jordan Example was referred for confidential treatment.'


class OutputGuardTests(unittest.TestCase):
    def test_benign_rules_only(self):
        self.assertEqual(output_guard.assess(BENIGN, use_model=False), {
            'action': 'no_signal', 'signals': [], 'model': 'disabled',
        })

    def test_rule_flag_skips_model_and_omits_secret(self):
        with patch.object(output_guard, 'model_verdict') as model:
            result = output_guard.assess(SYNTHETIC_SECRET)
        model.assert_not_called()
        self.assertEqual(result['action'], 'review')
        self.assertIn('labeled_secret', result['signals'])
        self.assertNotIn('DEMO_ONLY_FAKE_42', json.dumps(result))

    def test_model_protocol_and_fallback(self):
        responses = [('REVIEW', 'review', 'review'), ('CLEAR', 'no_signal', 'clear'),
                     ('unexpected response', 'no_signal', 'unavailable')]
        for content, action, model_status in responses:
            with self.subTest(content=content), patch.dict(os.environ, {
                'LLM_URL': 'http://127.0.0.1:8080/v1/', 'LLM_MODEL': 'fixture-model',
            }), patch.object(output_guard.http.client, 'HTTPConnection') as connect:
                connection = connect.return_value
                response = connection.getresponse.return_value
                response.status = 200
                response.read.return_value = json.dumps({'choices': [
                    {'message': {'content': content}},
                ]}).encode()
                result = output_guard.assess(SYNTHETIC_RECORD)
                self.assertEqual((result['action'], result['model']), (action, model_status))
                connect.assert_called_once_with('127.0.0.1', 8080, timeout=3)
                request = connection.request.call_args
                self.assertEqual(request.args, ('POST', '/v1/chat/completions'))
                payload = json.loads(request.kwargs['body'])
                self.assertEqual(payload['model'], 'fixture-model')
                self.assertEqual(json.loads(payload['messages'][1]['content']), {
                    'candidate_output': SYNTHETIC_RECORD,
                })
                connection.close.assert_called_once()

    def test_connection_failure(self):
        with patch.dict(os.environ, {'LLM_URL': 'http://127.0.0.1:8080/v1'}), patch.object(
            output_guard.http.client, 'HTTPConnection', side_effect=ConnectionRefusedError,
        ):
            result = output_guard.assess(BENIGN)
        self.assertEqual(result, {'action': 'no_signal', 'signals': [], 'model': 'unavailable'})

    def test_non_loopback_endpoint_is_skipped(self):
        with patch.dict(os.environ, {'LLM_URL': 'http://192.0.2.1:8080/v1'}), patch.object(
            output_guard.http.client, 'HTTPConnection',
        ) as connect:
            self.assertEqual(output_guard.assess(BENIGN)['model'], 'unavailable')
        connect.assert_not_called()

    def test_oversized_input_goes_to_review(self):
        with patch.object(output_guard, 'model_verdict') as model:
            result = output_guard.assess('x' * (output_guard.MAX_CHARS + 1))
        model.assert_not_called()
        self.assertEqual(result['signals'], ['input_too_large'])
        self.assertEqual(result['action'], 'review')

    def test_cli_exit_status(self):
        script = Path(__file__).with_name('output_guard.py')
        for text, status in [(BENIGN, 0), (SYNTHETIC_SECRET, 2)]:
            with self.subTest(status=status):
                result = subprocess.run([sys.executable, str(script), '--rules-only'],
                                        input=text, text=True, capture_output=True)
                self.assertEqual(result.returncode, status, result.stderr)
                self.assertEqual(json.loads(result.stdout)['model'], 'skipped' if status else 'disabled')


if __name__ == '__main__':
    unittest.main()
