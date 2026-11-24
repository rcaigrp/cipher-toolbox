import unittest
from safe_image_parser import parse_image_safely

class TestSafeParser(unittest.TestCase):
    
    def test_valid_image(self):
        # This would test with a known good image file
        result = parse_image_safely("test_image.png")
        self.assertTrue(result is not None)
        
    def test_invalid_file(self):
        # This would test with a malformed image file
        result = parse_image_safely("malformed_file.bin")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()