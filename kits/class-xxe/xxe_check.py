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
    
    # Parse the import statements to understand what's imported
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append((module, alias.name, alias.asname))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((None, alias.name, alias.asname))
    
    for call in calls:
        func = call.func
        full_name = None
        
        if isinstance(func, ast.Attribute):
            # Handle complex attribute chains like xml.etree.ElementTree.parse
            parts = []
            attr_node = func.value
            while isinstance(attr_node, ast.Attribute):
                parts.append(attr_node.attr)
                attr_node = attr_node.value
            if isinstance(attr_node, ast.Name):
                parts.append(attr_node.id)
            full_name = '.'.join(reversed(parts)) + '.' + func.attr
        elif isinstance(func, ast.Name):
            # Handle simple name like 'parse' in 'from xml.etree.ElementTree import parse'
            name = func.id
            # Check if this matches any imported function
            for module, imported_name, asname in imports:
                if imported_name == name and module == 'xml.etree.ElementTree':
                    full_name = f'{module}.{name}'
                elif imported_name == name and module == 'xml.dom.minidom':
                    full_name = f'{module}.{name}'
                elif imported_name == name and module == 'xml.sax':
                    full_name = f'{module}.{name}'
                elif imported_name == name and module == 'lxml.etree':
                    full_name = f'{module}.{name}'
                elif imported_name == name and module == 'xml.parsers.expat':
                    full_name = f'{module}.{name}'
        else:
            continue
            
        # If this is an XML parsing call, check for potential XXE issues
        if full_name and full_name in xml_functions:
            vulnerabilities.append((call.lineno, full_name))
    
    for lineno, func_name in vulnerabilities:
        print(f"Potential XXE vulnerability: {func_name} call at line {lineno}")
    
    return len(vulnerabilities)


def main():
    parser = argparse.ArgumentParser(description='Check Python files for potential XXE vulnerabilities')
    parser.add_argument('python_files', nargs='+', help='Python source files to check')
    args = parser.parse_args()

    total_vulnerabilities = 0
    for path in args.python_files:
        try:
            total_vulnerabilities += inventory(path)
        except Exception as e:
            print(f"Error processing {path}: {e}", file=sys.stderr)
            return 1

    return 0 if total_vulnerabilities == 0 else 1


if __name__ == '__main__':
    sys.exit(main())