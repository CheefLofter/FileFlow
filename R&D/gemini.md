The Rust project you shared, **Deadrop**, is a masterclass in combining several privacy technologies. To build a similar tool in **Python**, you can follow its blueprint.

The "Magic" of Deadrop isn't just encryption; it's the **Zero-Knowledge Architecture**: the server holds the encrypted file, but the decryption key is stored in the URL's `#fragment`, which—by web standards—is **never sent to the server**.

Here is how to build the Python version of this tool.

### 1. The Core Tech Stack
*   **Backend:** `FastAPI` (for the high-speed, async web server).
*   **Encryption:** `cryptography` (for AES-GCM or ChaCha20-Poly1305).
*   **Tunneling:** `python-libcloudflared` or a `subprocess` wrapper for Cloudflare's `cloudflared`.
*   **Frontend:** Plain HTML/JavaScript (to handle the `#fragment` decryption in the browser).

---

### 2. Step 1: Zero-Knowledge Encryption (Python)
You need to encrypt the file before it’s even ready to be served.

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def encrypt_file(file_path):
    key = ChaCha20Poly1305.generate_key() # 32 bytes
    cipher = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    ciphertext = cipher.encrypt(nonce, data, None)
    
    # We save the nonce + ciphertext, but NOT the key
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(nonce + ciphertext)
        
    return encrypted_file_path, key.hex()
```

### 3. Step 2: The "Blind" FastAPI Server
The server's only job is to serve an HTML page and the encrypted blob. It has no idea how to decrypt the blob.

```python
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI()
FILE_ID = "a3f9c1b2" # Generate this randomly
ENC_FILE = f"uploads/{FILE_ID}.enc"

@app.get(f"/d/{FILE_ID}")
async def download_page():
    # This HTML contains the Javascript that reads the #fragment
    return HTMLResponse(content=open("downloader.html").read())

@app.get(f"/api/raw/{FILE_ID}")
async def serve_bytes(background_tasks: BackgroundTasks):
    # Self-destruct logic: Delete after serving
    background_tasks.add_task(os.remove, ENC_FILE) 
    return FileResponse(ENC_FILE)
```

### 4. Step 3: Client-Side Decryption (JavaScript)
This is the most important part. The key is in the URL (e.g., `.../d/id#YOUR_HEX_KEY`). The browser extracts it using `window.location.hash`.

**downloader.html snippet:**
```javascript
async function decrypt() {
    const hexKey = window.location.hash.substring(1); // Get key from #
    const response = await fetch('/api/raw/a3f9c1b2');
    const arrayBuffer = await response.arrayBuffer();
    
    const nonce = arrayBuffer.slice(0, 12);
    const ciphertext = arrayBuffer.slice(12);

    // Use WebCrypto API to decrypt locally
    // No data is ever sent back to the server
    const key = await crypto.subtle.importKey("raw", hexToBytes(hexKey), "ChaCha20-Poly1305", false, ["decrypt"]);
    const decrypted = await crypto.subtle.decrypt({name: "ChaCha20-Poly1305", nonce}, key, ciphertext);
    
    // Trigger download of the decrypted blob
}
```

### 5. Step 4: Tunneling (The "Glob" part)
To make this available worldwide without port-forwarding, you can automate a **Cloudflare Tunnel** (just like Deadrop).

```python
import subprocess
import time

def start_tunnel(port):
    print("Opening Cloudflare Tunnel...")
    # This command requires cloudflared to be installed
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Parse the output to find the .trycloudflare.com URL
    for line in process.stdout:
        if "trycloudflare.com" in line:
            url = [word for word in line.split() if "trycloudflare.com" in word][0]
            return url
```

### 6. Step 5: Metadata Scrubbing
Before encrypting, use Python to remove identifying info (EXIF/GPS) from the file.

```python
from PIL import Image

def scrub_image(path):
    img = Image.open(path)
    data = list(img.getdata())
    img_no_exif = Image.new(img.mode, img.size)
    img_no_exif.putdata(data)
    img_no_exif.save(path) # Overwrites with clean data
```

### How the Final Tool Works:
1.  **User runs:** `python ded.py my_secret.pdf`
2.  **Local script:** Scrubs metadata → Encrypts file → Saves key locally.
3.  **Local script:** Starts FastAPI server → Starts Cloudflare Tunnel.
4.  **Local script:** Prints URL: `https://shiny-new-tunnel.trycloudflare.com/d/id#<KEY>`
5.  **Friend opens URL:** Their browser gets the HTML → JS reads the key from the URL hash → JS fetches the encrypted blob → **Decryption happens purely in their browser.**
6.  **Server:** Deletes the file immediately after the first download and shuts down.

### Why this is anonymous:
1.  **Zero Knowledge:** The Cloudflare tunnel and your Python server only ever see "Encrypted Noise."
2.  **No Logs:** Since the key is in the `#fragment`, it never appears in the server's access logs.
3.  **No Identity:** By using a "Quick Tunnel" (trycloudflare.com), you don't even need a Cloudflare account.
4.  **Tor (Optional):** You can use the `stem` library in Python to host this as a `.onion` service instead of using Cloudflare, providing even higher anonymity.