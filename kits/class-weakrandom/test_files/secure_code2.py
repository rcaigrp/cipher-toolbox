import secrets
import os

# All secure usage
token = secrets.token_hex(32)
secure_random = secrets.randbelow(1000)
os.urandom(16)