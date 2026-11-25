#!/usr/bin/env python3
"""
Security script to check for deserialization exposure patterns in code.
"""

import os
import re

def find_unsafe_deserialization_patterns(directory):
    """Find potential unsafe deserialization patterns."""
    unsafe_patterns = [
        # Python unsafe deserialization
        r'pickle\.loads?\s*\(',
        r'pickle\.load\s*\(',
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
    # This would be run against codebases or configurations
    print("Deserialization Exposure Check Script - Demo")
    print("This is a simplified check for demonstration purposes.")
    print("In practice, this would scan actual code repositories.")

if __name__ == "__main__":
    main()