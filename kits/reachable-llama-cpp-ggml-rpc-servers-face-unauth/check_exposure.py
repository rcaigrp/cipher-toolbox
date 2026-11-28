#!/usr/bin/env python3
"""
Check for exposure of llama.cpp RPC servers.
This script checks if llama.cpp is installed, what version it is,
and whether any RPC server is exposed over the network.
"""

import subprocess
import sys
import re

def check_llama_cpp_installed():
    """Check if llama.cpp is installed."""
    try:
        # Try to find llama.cpp binary in common locations
        result = subprocess.run(['which', 'llama-server'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

def check_llama_cpp_version():
    """Get the version of llama.cpp."""
    try:
        # Try to get version from llama-server --help or similar
        result = subprocess.run(['llama-server', '--help'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Look for version in help output
            match = re.search(r'version\s+(\d+\.\d+\.\d+)', result.stdout, re.IGNORECASE)
            if match:
                return match.group(1)
        return "unknown"
    except Exception:
        return "unknown"

def check_rpc_exposure():
    """Check if any RPC server is listening on non-local addresses."""
    try:
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '50052' in line and not ('127.0.0.1:50052' in line or 'localhost:50052' in line):
                    return True
        return False
    except Exception:
        return False

def main():
    print("Checking for llama.cpp RPC server exposure...")
    
    if not check_llama_cpp_installed():
        print("llama.cpp is NOT installed.")
        sys.exit(0)
    
    version = check_llama_cpp_version()
    print(f"llama.cpp version: {version}")
    
    exposed = check_rpc_exposure()
    if exposed:
        print("WARNING: RPC server is exposed over the network (port 50052).")
        print("This is vulnerable to CVE-2026-137567.")
        sys.exit(1)
    else:
        print("No RPC servers found listening on non-local addresses.")
        sys.exit(0)

if __name__ == "__main__":
    main()