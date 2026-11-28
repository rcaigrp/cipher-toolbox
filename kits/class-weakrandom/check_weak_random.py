#!/usr/bin/env python3
"""
Check for weak random number generation in Python code.
This script identifies potential uses of insecure random functions.
"""

import ast
import sys
import re

# List of insecure random functions that should be avoided
INSECURE_RANDOM_FUNCTIONS = {
    'random.random',
    'random.randint',
    'random.randrange',
    'random.choice',
    'random.shuffle',
    'random.sample',
    'random.uniform'
}

# List of secure alternatives
SECURE_RANDOM_FUNCTIONS = {
    'secrets.token_hex',
    'secrets.token_urlsafe',
    'secrets.randbelow',
    'os.urandom'
}

class WeakRandomChecker(ast.NodeVisitor):
    def __init__(self):
        self.weak_random_calls = []
        self.secure_random_calls = []
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            func_name = f"{node.func.value.id}.{node.func.attr}"
            if func_name in INSECURE_RANDOM_FUNCTIONS:
                self.weak_random_calls.append((func_name, node.lineno))
            elif func_name in SECURE_RANDOM_FUNCTIONS:
                self.secure_random_calls.append((func_name, node.lineno))
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in INSECURE_RANDOM_FUNCTIONS:
                self.weak_random_calls.append((func_name, node.lineno))
            elif func_name in SECURE_RANDOM_FUNCTIONS:
                self.secure_random_calls.append((func_name, node.lineno))
        
        self.generic_visit(node)

def check_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error in {filename}: {e}")
        return
    
    checker = WeakRandomChecker()
    checker.visit(tree)
    
    if checker.weak_random_calls:
        print(f"Weak random usage found in {filename}:")
        for func_name, line_num in checker.weak_random_calls:
            print(f"  Line {line_num}: {func_name}")
    
    if checker.secure_random_calls:
        print(f"Secure random usage found in {filename}:")
        for func_name, line_num in checker.secure_random_calls:
            print(f"  Line {line_num}: {func_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 check_weak_random.py <python_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    check_file(filename)