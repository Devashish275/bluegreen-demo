import os
from flask import Flask
app = Flask(__name__)
COLOR = os.getenv("APP_COLOR", "unknown")

@app.route("/")
def home():
    return f"<body style='background:{COLOR};color:white;text-align:center'><h1>Hello from {COLOR.upper()} - v1</h1></body>"

app.run(host="0.0.0.0", port=5000)
