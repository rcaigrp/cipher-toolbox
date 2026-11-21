# Toolbox Tools

This file lists the defensive tools that are part of the toolbox.

## File Parsing Tools

- **Description**: Defensive tools for safely parsing and validating files to prevent vulnerabilities.
- **Location**: `toolbox/file-parsing-tools`
- **Usage**: Run each script with `--help` for usage details. The tools include:
  - `buffer_safety.py`: Validates file contents against known unsafe patterns or structures.
  - `file_validation.py`: Ensures a file conforms to expected formats and sizes.
  - `safe_image_parser.py`: Safely parses image files without triggering vulnerabilities in image libraries.

Each tool is designed to be run in read-only mode by default, with an optional `--apply` flag for actions that modify the system (e.g., logging or quarantining unsafe files).