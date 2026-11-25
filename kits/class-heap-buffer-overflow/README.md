# Heap Buffer Overflow Class Analysis

This kit analyzes the heap buffer overflow vulnerability class, particularly in file parsing components.

## Files

- `FORESIGHT.md`: Complete analysis of the pattern and its implications
- `check_exposure.py`: Read-only script to detect exposure to this class
- `detection_rules/`: Detection rules for this vulnerability class

## Usage

Run the exposure check script to see if your system has processes that might be vulnerable:

```bash
python3 check_exposure.py
```

The script performs a read-only check and will identify any running file parsing processes.