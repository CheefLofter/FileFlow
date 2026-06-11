from flask import Flask
from flask_cloudflared import run_with_cloudflared, get_cloudflared_url

app = Flask(__name__)

# Automatically starts a TryCloudflare tunnel
run_with_cloudflared(app)

@app.route("/")
def home():
    # Retrieve the generated public URL
    url = get_cloudflared_url()
    return f"Hello World! Accessible at: {url}"

if __name__ == '__main__':
    app.run()   