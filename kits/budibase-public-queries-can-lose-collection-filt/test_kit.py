#!/usr/bin/env python3
"""Test the Budibase kit with sample data."""

import subprocess
import sys

def run_check_exposure():
    print("Testing check_exposure.py...")
    
    # Test --help
    result = subprocess.run([
        sys.executable, 'check_exposure.py', '--help'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"check_exposure.py --help failed: {result.stderr}"
    print("✅ check_exposure.py --help works")
    
    # Test with version file
    result = subprocess.run([
        sys.executable, 'check_exposure.py', '--version-path', 'test_fixtures/version.json'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"check_exposure.py version check failed: {result.stderr}"
    assert "Version: 3.9.1 falls below the vendor-stated 4.0.0 fix" in result.stdout
    print("✅ check_exposure.py with version file works")
    
    # Test with config file
    result = subprocess.run([
        sys.executable, 'check_exposure.py', '--config-path', 'test_fixtures/config.json'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"check_exposure.py config check failed: {result.stderr}"
    assert "Public MongoDB queries inventoried: 1" in result.stdout
    print("✅ check_exposure.py with config file works")
    
    # Test with both files
    result = subprocess.run([
        sys.executable, 'check_exposure.py', 
        '--version-path', 'test_fixtures/version.json',
        '--config-path', 'test_fixtures/config.json'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"check_exposure.py combined check failed: {result.stderr}"
    assert "Version: 3.9.1 falls below the vendor-stated 4.0.0 fix" in result.stdout
    assert "Public MongoDB queries inventoried: 1" in result.stdout
    print("✅ check_exposure.py with both files works")

def run_mitigate():
    print("Testing mitigate.py...")
    
    # Test --help
    result = subprocess.run([
        sys.executable, 'mitigate.py', '--help'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"mitigate.py --help failed: {result.stderr}"
    print("✅ mitigate.py --help works")
    
    # Test with required args
    result = subprocess.run([
        sys.executable, 'mitigate.py', 
        '--query-path', '/api/public/mongodb/fixture-public-mongodb-query',
        '--output', 'test_output.conf'
    ], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"mitigate.py dry run failed: {result.stderr}"
    assert "DRY RUN: Would create test_output.conf" in result.stdout
    print("✅ mitigate.py dry run works")
    
    # Clean up
    import os
    if os.path.exists('test_output.conf'):
        os.remove('test_output.conf')

if __name__ == '__main__':
    try:
        run_check_exposure()
        run_mitigate()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)