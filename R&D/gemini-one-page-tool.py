

import os
import secrets
import subprocess
import threading
from flask import Flask, send_from_directory, render_template_string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)

# CONFIGURATION
FILE_TO_SHARE = "gemini.md"  # Change this to your file
DROP_ID = secrets.token_hex(8)
KEY = AESGCM.generate_key(bit_length=256)
NONCE = os.urandom(12)

# 1. ENCRYPT FILE LOCALLY
def prepare_file():
    aesgcm = AESGCM(KEY)
    with open(FILE_TO_SHARE, "rb") as f:
        data = f.read()
    ciphertext = aesgcm.encrypt(NONCE, data, None)
    
    # Save the encrypted version
    with open(f"{DROP_ID}.enc", "wb") as f:
        f.write(NONCE + ciphertext)
    print(f"[*] File encrypted. Original size: {len(data)} bytes")

# 2. THE BLIND SERVER (DOWNLOAD PAGE)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Secure Drop</title></head>
<body style="font-family:sans-serif; text-align:center; padding-top:50px;">
    <h1>You have a secure file drop</h1>
    <p>Decryption happens in your browser. The server sees nothing.</p>
    <button id="dl" style="padding:15px 30px; font-size:20px; cursor:pointer;">Decrypt & Save File</button>

    <script>
        document.getElementById('dl').onclick = async () => {
            const keyHex = window.location.hash.substring(1);
            if (!keyHex) { alert("No key found in URL!"); return; }

            const response = await fetch('/raw');
            const blob = await response.arrayBuffer();
            
            const nonce = blob.slice(0, 12);
            const ciphertext = blob.slice(12);

            // Import the key from the URL fragment
            const rawKey = new Uint8Array(keyHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
            const cryptoKey = await crypto.subtle.importKey("raw", rawKey, "AES-GCM", false, ["decrypt"]);

            try {
                const decrypted = await crypto.subtle.decrypt({name: "AES-GCM", nonce: nonce}, cryptoKey, ciphertext);
                const url = window.URL.createObjectURL(new Blob([decrypted]));
                const a = document.createElement('a');
                a.href = url;
                a.download = "decrypted_file";
                a.click();
                alert("File decrypted! This link is now dead.");
            } catch (e) {
                alert("Decryption failed. Wrong key or corrupted data.");
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/raw')
def raw():
    # Serve the encrypted file and then SHUT DOWN
    @app.after_request
    def cleanup(response):
        threading.Thread(target=lambda: os._exit(0)).start() # Kill server after 1 download
        return response
    return send_from_directory(".", f"{DROP_ID}.enc")

# 3. GLOBAL TUNNEL
def start_tunnel():
    print("[*] Starting Global Tunnel...")
    # This opens a public URL without port forwarding
    tunnel = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://127.0.0.1:5000"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in tunnel.stdout:
        if "trycloudflare.com" in line:
            url = [w for w in line.split() if "trycloudflare.com" in w][0]
            print(f"\n[!] SHARE THIS LINK:\n{url}/#{KEY.hex()}\n")
            break

if __name__ == "__main__":
    prepare_file()
    threading.Thread(target=start_tunnel).start()
    app.run(port=5000, debug=False)
