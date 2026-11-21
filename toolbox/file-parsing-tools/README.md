# File Parsing Security Toolkit

This toolbox contains defensive tools for protecting against file parsing vulnerabilities.

## Contents

- `safe_image_parser.py` - A sandboxed image parser with strict validation
- `file_validation.py` - File type and size validation utilities  
- `buffer_safety.py` - Buffer overflow prevention utilities

## Usage

These tools are designed to be integrated into applications that process user-uploaded files. They provide:

1. **Strict file format validation** before parsing
2. **Size limits** for all file components
3. **Sandboxed execution** for file processing
4. **Buffer safety checks** to prevent overflows

## Integration

To use these tools, import the relevant modules and apply them to your file processing pipeline:

```python
from file_validation import validate_file_type
from safe_image_parser import parse_image_safely

# Validate before processing
if validate_file_type(file_path):
    # Parse safely
    result = parse_image_safely(file_path)
```

## Testing

Run tests with:
```bash
python -m pytest test/
```