import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.encryption import encrypt_zip

with open("test-files/test-empty.zip", "rb") as f:
    raw = f.read()

blob, key_fragment = encrypt_zip(raw)

print(key_fragment)