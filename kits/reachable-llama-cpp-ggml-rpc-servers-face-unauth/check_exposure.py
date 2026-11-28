#!/usr/bin/env python3
"""
Security exposure checker - fixed version with issues resolved.
"""

import argparse
import os  # This was the first issue: missing import

def check_root():
    """Check if running as root."""
    # Fixed: 'os' was undefined in original code, now properly imported
    if os.geteuid() == 0:
        return True
    return False

def check_netstat():
    """Check for specific port exposure using netstat."""
    try:
        import subprocess
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        # Fixed: The syntax error was in a line that had 'if '50052' in lin' - 
        # this was likely a truncated or malformed line
        for line in lines:
            if '50052' in line:  # Fixed: complete and correct syntax
                print(f"Port 50052 is exposed: {line.strip()}")
                return True
        return False
    except Exception as e:
        print(f"Error checking netstat: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check for security exposures.")
    parser.add_argument("--check-root", action="store_true", help="Check if running as root")
    parser.add_argument("--check-netstat", action="store_true", help="Check netstat for port exposure")
    
    args = parser.parse_args()
    
    if args.check_root:
        if check_root():
            print("Running as root - this may be a security risk.")
        else:
            print("Not running as root - good.")
    
    if args.check_netstat:
        check_netstat()

if __name__ == "__main__":
    main()