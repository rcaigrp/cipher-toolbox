# File Parsing Vulnerability Class

## Pattern Analysis

The recent Krita vulnerabilities (ZDI-26-1010 through ZDI-26-1014) demonstrate a recurring pattern in file parsing libraries:

- **Integer Overflow/Underflow**: PSB, ASL files
- **Buffer Overflow**: ABR, JC2 files  
- **Out-of-Bounds Write**: TIFF files

All these vulnerabilities stem from the same root cause: improper validation of user-supplied file data during parsing. These are classic buffer overflow and integer overflow issues that can lead to remote code execution.

## Why More Are Coming

This class is highly persistent because:

1. **Common Design Pattern**: File parsers often reuse similar code structures for handling variable-length data
2. **Complexity Increases Risk**: As formats become more complex, so does the potential for miscalculation in size/length fields
3. **Legacy Code**: Many file format libraries have been maintained for years without modern security practices

## Products Likely Next

Based on variant analysis of vulnerable components:

1. **Graphics Libraries**:
   - ImageMagick (uses similar parsing logic)
   - GraphicsMagick 
   - FreeImage
   - OpenJPEG (seen in JC2 vulnerability)

2. **Office/Document Parsers**:
   - LibreOffice
   - Apache POI (Java)
   - Microsoft Office (OOXML, DOCX)
   - PDF libraries (Poppler, MuPDF)

3. **Media Processing Tools**:
   - FFmpeg (uses OpenJPEG)
   - Video editing software (DaVinci Resolve, Blender)
   - Audio processing tools

4. **CAD/Engineering Software**:
   - AutoCAD
   - SolidWorks
   - FreeCAD
   - Rhino 3D

5. **Other Image/Document Libraries**:
   - Skia
   - Cairo
   - Qt Graphics

## Early Warning Signs to Watch

- Files with variable-length fields or embedded data structures
- Use of third-party libraries like OpenJPEG, libpng, libtiff
- Complex file format specifications (e.g., PSD, PSB, TIFF)
- Recent security fixes in image processing libraries
- CVEs related to integer overflows or buffer overflows in file parsers

## What to Prepare Now

1. **Hardening**:
   - Disable file parsing for untrusted sources if possible
   - Implement strict file validation (file type detection, size limits)
   - Use sandboxed environments for file processing

2. **Monitoring**:
   - Monitor for unusual file access patterns or large file uploads
   - Log file parsing operations with metadata (size, type, source)

3. **Inventory Questions**:
   - What third-party libraries do we use that parse external files?
   - Which applications process image/document files from untrusted users?
   - Are our file parsers hardened against integer overflows?

4. **Detection Rules**:
   - Sigma rules to detect large buffer allocations or suspicious file sizes
   - YARA rules for known vulnerable library versions
   - Network monitoring for file upload patterns

## Class-Wide Detections

### Sigma Rules
```yaml
title: Out-of-Bounds Write in File Parsing
id: 8b3c12a7-5e8a-4d90-ba6f-3258a54f1a91
status: experimental
description: Detects potential out-of-bounds writes in file parsing libraries
author: Cipher
date: 2026-11-20
logsource:
    category: application
    product: graphics_library
detection:
    selection:
        event_id: 1001
        message: contains 'buffer overflow'
    condition: selection
fields:
    - process_name
    - file_path
    - error_code
falsepositives:
    - Legitimate large image processing operations
level: high
```

### YARA Rules
```yara
rule FileParsingBufferOverflow {
    meta:
        description = "Detects potential buffer overflow in file parsing"
        author = "Cipher"
        date = "2026-11-20"
    
    strings:
        $overflow_pattern = /buffer_overflow|out_of_bounds_write/i
        $integer_overflow = /integer_overflow|signed_integer_overflow/i
    
    condition:
        $overflow_pattern or $integer_overflow
}
```

### Check Script
```bash
#!/bin/bash
# File parsing exposure check

echo "Checking for vulnerable file parsing libraries..."

# Check if ImageMagick is installed (commonly vulnerable)
if command -v identify &> /dev/null; then
    echo "ImageMagick identified"
    # Check version
    identify -version | grep -i "version"
fi

# Check for known vulnerable library files in common paths
for lib_path in "/usr/lib" "/usr/local/lib" "/opt"; do
    if [ -d "$lib_path" ]; then
        find "$lib_path" -name "*jpeg*" -o -name "*tiff*" -o -name "*png*" 2>/dev/null | head -5
    fi
done

echo "Check complete. Review results for any vulnerable libraries."
```

This vulnerability class is likely to continue appearing because it's a fundamental flaw in how file parsers handle user input, and the same design patterns are repeated across many libraries.

TOPIC: File Parsing Vulnerabilities