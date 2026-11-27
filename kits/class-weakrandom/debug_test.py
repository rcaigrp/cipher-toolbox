#!/usr/bin/env python3

import ast
import sys

# Simple test to debug AST parsing
code = """
import random
x = random.randint(1, 10)
y = random.random()
"""

tree = ast.parse(code)

print("AST nodes:")
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        print(f"Call node: {ast.dump(node)}")
        if isinstance(node.func, ast.Attribute):
            print(f"  Attribute access: {node.func.attr}")
            print(f"  Value: {ast.dump(node.func.value)}")