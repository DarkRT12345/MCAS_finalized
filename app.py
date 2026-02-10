from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import os

from testsummary import generate_summary  # 👈 import your ML function

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/Multimedia-Content-Analysing-System"
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/summarypagefortext')
def summarypagefortext():
    return render_template('summarypagefortext.html')

@app.route('/generate_text_summary', methods=['POST'])
def generate_text_summary():
    data = request.get_json()
    user_text = data.get("text")

    if not user_text or not user_text.strip():
        return jsonify({"error": "Enter some text"}), 400

    try:
        summary = generate_summary(user_text)   # 🚀 fast call
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
