# Weak Random Number Generation Checker

This tool checks Python source code for weak random number generation patterns that could lead to security vulnerabilities.

## Usage

```bash
python3 check_weak_random.py [FILE]
```

Checks FILE for weak random number generation patterns.
If no FILE is provided, checks stdin or shows this help.

## Detection Patterns

The tool looks for these insecure patterns:
- `random.randint()`
- `random.random()` 
- `random.choice()`
- `rand()`
- `srand()`

## Example

```bash
# Check a file
python3 check_weak_random.py my_script.py

# Check from stdin
cat my_script.py | python3 check_weak_random.py
```

## Security Recommendation

Replace insecure random usage with the `secrets` module for cryptographically secure randomness:

```python
import secrets

# Instead of: import random; random.randint(1, 10)
# Use:    import secrets; secrets.randbelow(10) + 1
```