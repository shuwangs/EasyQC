from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configure the dir for the later use

UPLOAD_FOLDER = 'backend/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Welcome to EasyQC! Please upload your CSV file for data quality checks."

@app.route('/upload', methods=['POST'])
def upload_file():
    # TODO:
    file = request.files['file']


if __name__ == '__main__':
    app.run(debug=True)