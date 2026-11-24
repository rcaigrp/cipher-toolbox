import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_exposure import check_endpoint, main

class TestAuthBypass(unittest.TestCase):
    
    @patch('check_exposure.requests.get')
    def test_check_endpoint_success(self, mock_get):
        # Mock a successful request with status code 200
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = check_endpoint("http://test.com/api/test")
        self.assertEqual(result, 200)
    
    @patch('check_exposure.requests.get')
    def test_check_endpoint_failure(self, mock_get):
        # Mock a failed request
        mock_get.side_effect = Exception("Connection error")
        
        result = check_endpoint("http://test.com/api/test")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()