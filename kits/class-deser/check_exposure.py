#!/usr/bin/env python3
"""
Security script to check for deserialization exposure patterns in code.
"""

import argparse
import os
import re

def find_unsafe_deserialization_patterns(directory):
    """Find potential unsafe deserialization patterns."""
    unsafe_patterns = [
        # Python unsafe deserialization
        r'pickle\.loads?\s*\(',
        r'yaml\.load\s*\(',
        r'json\.loads?\s*\(',  # Potentially dangerous if used with untrusted data
        
        # Java unsafe deserialization
        r'ObjectInputStream\.readObject\s*\(',
        r'org\.apache\.commons\.collections',
        
        # PHP unsafe deserialization  
        r'unserialize\s*\(',
        
        # Node.js unsafe deserialization
        r'deserialize\s*\(',
        r'node-serialize',
        
        # C# unsafe deserialization
        r'System\.Runtime\.Serialization\.Formatters',
    ]
    
    findings = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.java', '.php', '.js', '.cs')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern in unsafe_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            findings.append({
                                'file': filepath,
                                'line': line_num,
                                'pattern': pattern,
                                'context': content[max(0, match.start()-30):match.end()+30]
                            })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return findings

def main():
    parser = argparse.ArgumentParser(description="Check source files for potential deserialization exposure patterns.")
    parser.add_argument("directory", help="directory containing source files to scan")
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        parser.error(f"{args.directory!r} is not a directory")

    findings = find_unsafe_deserialization_patterns(args.directory)
    if not findings:
        print("No potential deserialization exposure patterns found.")
        return

    print("Potential deserialization exposure patterns found:")
    for finding in findings:
        print(f"File: {finding['file']}, Line: {finding['line']}")
        print(f"Pattern: {finding['pattern']}")
        print(f"Context: {finding['context']}")
        print("---")


if __name__ == "__main__":
    main()
