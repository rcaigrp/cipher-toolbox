#!/usr/bin/env python3
"""Inventory Python code for potential XXE vulnerabilities."""

import argparse
import ast
from pathlib import Path
import sys


def inventory(path):
    with open(path, 'r') as source:
        tree = ast.parse(source.read(), filename=str(path))

    # Look for XML parsing related functions
    xml_functions = {
        'xml.etree.ElementTree.parse',
        'xml.dom.minidom.parse',
        'xml.sax.parse',
        'lxml.etree.parse',
        'xml.parsers.expat.ParserCreate'
    }
    
    calls = sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.Call)),
        key=lambda node: (node.lineno, node.col_offset),
    )
    
    vulnerabilities = []
    
    for call in calls:
        func = call.func
        if isinstance(func, ast.Attribute):
            full_name = f"{func.value.id}.{func.attr}" if isinstance(func.value, ast.Name) else str(func)
        elif isinstance(func, ast.Name):
            full_name = func.id
        else:
            continue
            
        # If this is an XML parsing call, check for potential XXE issues
        if full_name in xml_functions:
            vulnerabilities.append((call.lineno, full_name))
    
    for lineno, func_name in vulnerabilities:
        print(f"Potential XXE vulnerability: {func_name} call at line {lineno}")
    
    return len(vulnerabilities)


def main():
    parser = argparse.ArgumentParser(description='Check Python files for potential XXE vulnerabilities')
    parser.add_argument('python_files', nargs='+', help='Python source files to check')
    args = parser.parse_args()
    
    total_vulns = 0
    for file_path in args.python_files:
        try:
            vulns = inventory(file_path)
            total_vulns += vulns
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)
            return 1
    
    return 0 if total_vulns == 0 else 1


if __name__ == '__main__':
    sys.exit(main())