import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM





def encrypt_zip(file_bytes: bytes) -> tuple[bytes, str]:

    """encryption using AESGM

        usage->

        with open("file.zip", "rb") as f:
            raw = f.read()

        blob, key_fragment = encrypt_zip(raw)

        the funcrion encrypts the file and returns the blob and key_fragment

        the key fragment is base64 encoded
        -> key_b64 = base64.urlsafe_b64encode(key).decode()


    """
    
    key = os.urandom(32)          #256-bit 
    iv  = os.urandom(12)          #96-bit nonce 
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, file_bytes, None)  
    blob = iv + ciphertext        
    key_b64 = base64.urlsafe_b64encode(key).decode()
    return blob, key_b64


if __name__ == "__main__":

    with open("file.zip", "rb") as f:
        raw = f.read()

    blob, key_fragment = encrypt_zip(raw)
