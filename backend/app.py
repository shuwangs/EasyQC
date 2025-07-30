from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configure the dir for the later use

UPLOAD_FOLDER = 'backend/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

