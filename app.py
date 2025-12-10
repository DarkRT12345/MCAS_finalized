from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import subprocess

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Multimedia-Content-Analysing-System"
app.config["UPLOAD_FOLDER"] = "static/uploads"
mongo = PyMongo(app)
app.secret_key = "9b1c8c49d3c3e7e456f7ab97d8332a19"
bcrypt = Bcrypt(app)
users_collection = mongo.db.users

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('Homepage.html')  


@app.route('/textsummary')
def textsummary():
    return render_template('textsummary.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/summarypagefortext')
def summarypagefortext():
    return render_template('summarypagefortext.html')



@app.route('/generate_text_summary', methods=['POST'])
def generate_text_summary():
    data = request.get_json()  # Get JSON data from the request
    user_text = data.get("text")  # Extract text from JSON

    if not user_text or not user_text.strip():
        return jsonify({"error": "Enter some text"}), 400

    try:
        # Run testsummary.py and send the text via stdin
        result = subprocess.run(
            ['python', 'testsummary.py'],
            input=user_text,  # Pass the text as input
            capture_output=True,
            text=True
        )

        summary = result.stdout.strip()

        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    data = request.get_json()
    video_id = data.get("videoId")

    if not video_id:
        return jsonify({"error": "Invalid video ID"}), 400

    try:
        result  = subprocess.run(['python', 'summarytest.py', video_id], capture_output=True, text=True)
        summary = result.stdout.strip()  # Capture the output summary

        return jsonify({"summary": summary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    
    app.run(debug=True)