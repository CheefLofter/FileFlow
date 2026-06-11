from flask import Flask, render_template

from flask import request

from src.encryption import encrypt_zip
#import base64



app = Flask(__name__)

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
    #print("Key Fragment:", key_fragment)
    #blob_b64 = base64.urlsafe_b64encode(blob).decode()
    return key_fragment, 200


   

if __name__ == "__main__":
    app.run(debug=True)