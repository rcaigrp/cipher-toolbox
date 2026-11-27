#!/usr/bin/env python3
"""Inventory Python code for potential SSRF vulnerabilities."""

import argparse
import ast
from pathlib import Path
import sys


def inventory(path):
    with open(path, 'r') as source:
        tree = ast.parse(source.read(), filename=str(path))

    # Look for HTTP request related functions
    http_functions = {
        'urllib.request.urlopen',
        'requests.get', 
        'requests.post',
        'requests.put',
        'requests.delete',
        'http.client.HTTPConnection',
        'httplib.HTTPConnection'
    }
    
    calls = sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.Call)),
        key=lambda node: (node.lineno, node.col_offset),
    )
    
    # Find all assignments to variables
    assignments = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) > 0:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                assignments[target.id] = node.value
    
    vulnerabilities = []
    
    for call in calls:
        func = call.func
        if isinstance(func, ast.Attribute):
            full_name = f"{func.value.id}.{func.attr}" if isinstance(func.value, ast.Name) else str(func)
        elif isinstance(func, ast.Name):
            full_name = func.id
        else:
            continue
            
        # If this is an HTTP call, check if any argument comes from user input
        if full_name in http_functions or any(funct in full_name for funct in ['requests', 'urllib']):
            for arg in call.args:
                if isinstance(arg, ast.Name):
                    arg_name = arg.id
                    # Check if this variable was assigned from a user input function
                    if arg_name in assignments:
                        assign_node = assignments[arg_name]
                        if isinstance(assign_node, ast.Call) and isinstance(assign_node.func, ast.Name):
                            func_name = assign_node.func.id
                            if func_name in ['input', 'get', 'request']:
                                vulnerabilities.append((call.lineno, full_name, arg_name))
    
    for lineno, func_name, arg_name in vulnerabilities:
        print(f"Potential SSRF vulnerability: {func_name} call at line {lineno} uses variable '{arg_name}' which comes from user input")
    
    return len(vulnerabilities)


def main():
    parser = argparse.ArgumentParser(description='Check Python files for potential SSRF vulnerabilities')
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