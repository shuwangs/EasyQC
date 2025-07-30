from flask import Flask, request, jsonify
import os, uuid

app = Flask(__name__)

# Configure the dir for the later use

UPLOAD_FOLDER = '/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_NORMALIZATIONS = ['tic', 'is', 'qc', 'pqn', 'is+qc', 'is+pqn']

@app.route('/')
def index():
    return "Welcome to EasyQC! Please upload your CSV file for data quality checks."

@app.route('/upload', methods=['POST'])
def upload_file():
    # TODO:
    if 'file' not in request.files:
        return jsonify({'Error': 'No file provided'}), 400
    
    file = request.files['file']

    normalization = request.form.get('normalization', "none").lower()
    if normalization not in ALLOWED_NORMALIZATIONS:
        return jsonify({'Error': f'Invalid normalization method: {normalization}'}), 400

    if file and file.filename.lower().endswith('.txt'):
        filename = f"{uuid.uuid4().hex}.txt"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "normalization": normalization
        }), 200

    return jsonify({'error': 'Only CSV files are allowed'}), 400
 



if __name__ == '__main__':
    app.run(debug=True)