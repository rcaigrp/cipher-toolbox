#!/usr/bin/env python3
"""
Check for Netis WF2409E management exposure.

This script inventories local TCP listeners on HTTP(S) management ports
without making network requests, similar to the shell version but in Python.
"""

import subprocess
import sys

def check_exposure():
    """Check for local TCP listeners on management ports."""
    
    # Define the management ports
    ports = [80, 443, 8080, 8443]
    
    # Build ss command
    port_args = ' or '.join([f"sport = :{port}" for port in ports])
    cmd = ["ss", "-H", "-ltn", f"( {port_args} )"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        listeners = result.stdout.strip()
        
        if not listeners:
            print('VERDICT: NO MATCHING LOCAL TCP LISTENERS on ports 80, 443, 8080, or 8443.')
            return
        
        print(listeners)
        
        # Check if any listener is bound beyond loopback
        lines = listeners.split('\n')
        non_loopback_found = False
        
        for line in lines:
            if not line.strip():
                continue
                
            # Extract the local address (4th field in ss output)
            parts = line.split()
            if len(parts) >= 4:
                local_addr = parts[3]
                if not (local_addr.startswith('127.') or local_addr.startswith('[::1]:')):
                    non_loopback_found = True
                    break
        
        if non_loopback_found:
            print('VERDICT: REVIEW. At least one matching listener is bound beyond loopback. Verify its owner and firewall policy.')
        else:
            print('VERDICT: Matching listeners bind only to loopback.')
            
    except subprocess.CalledProcessError as e:
        print(f'VERDICT: UNKNOWN. Could not inspect local listeners: {e}', file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print('VERDICT: UNKNOWN. ss (iproute2) is required to inspect local listeners.', file=sys.stderr)
        sys.exit(2)

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print('Usage: python3 check_exposure.py. Inventory local TCP listeners on HTTP(S) management ports without making network requests.')
            return
        else:
            print('Usage: python3 check_exposure.py', file=sys.stderr)
            sys.exit(2)

    check_exposure()
    print('Router identity, WAN management, upstream forwarding, and internet reachability require separate verification from existing inventory or configuration records.')
    print('Firmware verdict: UNKNOWN. Record the exact model, hardware revision, and installed firmware from existing records. The supplied material identifies no verified fixed release for comparison.')

if __name__ == '__main__':
    main()
