#!/usr/bin/env python3
import os
import sys

def check_krita_exposure():
    """Check if Krita is installed and might be exposed to vulnerabilities"""
    
    # Common installation paths
    krita_paths = [
        "/usr/bin/krita",
        "/usr/local/bin/krita",
        "C:\\Program Files\\Krita\\bin\\krita.exe"
    ]
    
    for path in krita_paths:
        if os.path.exists(path):
            print(f"Krita found at: {path}")
            return True
    
    print("No Krita installation found")
    return False

if __name__ == "__main__":
    check_krita_exposure()