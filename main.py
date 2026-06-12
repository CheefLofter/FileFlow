from flask import Flask, render_template
from flask import request
from src.encryption import encrypt_zip
import base64
from flask_cloudflared import run_with_cloudflared, get_cloudflared_url

storage = {"blob": None, "filename": None, "key": None}

app = Flask(__name__)

# Automatically starts a TryCloudflare tunnel
run_with_cloudflared(app)

@app.route("/")
@app.route("/send")
def Upload():
    return render_template("sender.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    # Read file content into memory (bytes)
    raw = file.read()

    blob, key_fragment = encrypt_zip(raw)

    storage["blob"] = blob
    storage["filename"] = file.filename
    storage["key"] = key_fragment

    #print("Key Fragment:", key_fragment)
    #blob_b64 = base64.urlsafe_b64encode(blob).decode()
    url = get_cloudflared_url()
    return f"Hello World! Accessible at: {url}/download#key={key_fragment}"



@app.route("/download")
def download_file():
    blob = storage["blob"]
    filename = storage["filename"]
    if not blob:
        return "No file available", 404

    blob_b64 = base64.b64encode(blob).decode()
    #print(storage["key"])
    return render_template("receiver.html", blob_b64=blob_b64,filename=storage["filename"])
    


   

if __name__ == "__main__":
    app.run(debug=True)


    #NameError: name 'blob' is not defined