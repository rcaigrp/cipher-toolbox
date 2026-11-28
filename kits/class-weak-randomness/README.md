# Class Weak Randomness Detector

This tool detects weak random number generation patterns in code, particularly focusing on insecure randomness functions that should be replaced with secure alternatives.

## Features

- Detects `rand()`, `random.randint()`, `random.random()`, etc.
- Supports both Python and C/C++ files
- Identifies insecure random usage patterns

## Usage

```bash
python3 check_weak_random.py <file>
```

The tool will return:
- Exit code 0 if no weak randomness is found
- Exit code 1 with error messages if weak randomness is detected

## Examples

### Python Example

```python
import random
x = random.randint(1, 100)  # This will be flagged
```

### C Example

```c
#include <stdlib.h>
int main() {
    int x = rand();  // This will be flagged
}
```

## Secure Alternatives

For Python:
- Use `secrets` module instead of `random`
- Example: `import secrets; secure_random = secrets.token_hex(16)`

For C:
- Use `getrandom()` or similar secure functions instead of `rand()`

## Test Files

The following test files are included to demonstrate functionality:

- `test_file.py`: Contains insecure random usage
- `test_secure.py`: Contains secure random usage
- `test_weak.py`: Contains insecure random usage (Python)
- `test_file.c`: Contains insecure random usage (C)
- `test_secure.c`: Contains secure random usage (C)
- `test_weak.c`: Contains insecure random usage (C)
- `test_mixed.py`: Mix of secure and insecure random usage

Run tests with:
```bash
python3 check_weak_random.py test_file.py
python3 check_weak_random.py test_secure.py
python3 check_weak_random.py test_weak.py
python3 check_weak_random.py test_file.c
python3 check_weak_random.py test_secure.c
python3 check_weak_random.py test_weak.c
python3 check_weak_random.py test_mixed.py
```