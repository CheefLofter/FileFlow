from src.encryption import encrypt_zip



with open("test-files/test-empty.zip", "rb") as f:
    raw = f.read()

blob, key_fragment = encrypt_zip(raw)

print(key_fragment)