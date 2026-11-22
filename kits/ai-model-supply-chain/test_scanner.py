import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

from scanner import DEFAULT_LLM_URL, scan_model_file


class ScannerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / 'synthetic.safetensors'
        self.benign = b'\x10\x00\x00\x00\x00\x00\x00\x00{"fixture":true}'
        self.path.write_bytes(self.benign)

    def test_rules_only_benign_looking_fixture_and_digest(self):
        with patch('scanner.build_opener') as build_opener:
            result = scan_model_file(self.path, use_model=False)
        build_opener.assert_not_called()
        self.assertEqual(result['sha256'], hashlib.sha256(self.benign).hexdigest())
        self.assertEqual(result['status'], 'NO_SIGNAL')
        self.assertEqual(result['model_status'], 'disabled')

    def test_pickle_marker_under_safetensors_name(self):
        self.path.write_bytes(b'\x80\x04INERT FIXTURE')
        result = scan_model_file(self.path, use_model=False)
        self.assertEqual(result['status'], 'REVIEW')
        self.assertIn('Header resembles binary pickle', result['findings'])

    def test_default_endpoint_can_escalate_without_receiving_file_data(self):
        response = {'choices': [{'message': {'content': 'REVIEW'}}]}
        with patch.dict(os.environ, {}, clear=True), patch('scanner.build_opener') as build_opener:
            open_request = build_opener.return_value.open
            open_request.return_value = io.BytesIO(json.dumps(response).encode())
            result = scan_model_file(self.path)
        request = open_request.call_args.args[0]
        self.assertEqual(request.full_url, DEFAULT_LLM_URL + '/chat/completions')
        metadata = json.loads(json.loads(request.data)['messages'][1]['content'])
        self.assertEqual(set(metadata), {'extension_category', 'header_signature', 'rule_findings'})
        self.assertEqual(result['status'], 'REVIEW')
        self.assertEqual(result['model_status'], 'REVIEW')

    def test_unavailable_model_preserves_rule_findings(self):
        self.path.write_bytes(b'\x7fELFINERT FIXTURE')
        with patch('scanner.build_opener') as build_opener:
            build_opener.return_value.open.side_effect = URLError('offline')
            result = scan_model_file(self.path)
        self.assertEqual(result['status'], 'REVIEW')
        self.assertEqual(result['model_status'], 'unavailable')

    def test_model_cannot_clear_rule_findings(self):
        self.path.write_bytes(b'PK\x03\x04INERT FIXTURE')
        response = {'choices': [{'message': {'content': 'NO_ADDITIONAL_SIGNAL'}}]}
        with patch('scanner.build_opener') as build_opener:
            build_opener.return_value.open.return_value = io.BytesIO(json.dumps(response).encode())
            result = scan_model_file(self.path)
        self.assertEqual(result['status'], 'REVIEW')
        self.assertEqual(result['model_status'], 'NO_ADDITIONAL_SIGNAL')


if __name__ == '__main__':
    unittest.main()
