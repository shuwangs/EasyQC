from flask import Flask, request, jsonify
from utils.run_r_scripts import run_all_r_scripts
import os, uuid

app = Flask(__name__)

# Configure the dir for the later use
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "uploads"))
RESULT_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "results"))
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
os.makedirs(RESULT_FOLDER, exist_ok = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER


ALLOWED_NORMALIZATIONS = ['tic', 'is', 'qc', 'pqn', 'is+qc', 'is+pqn', 'none']

@app.route('/')
def index():
    return "Welcome to EasyQC! Please upload your CSV file for data quality checks."

@app.route('/upload', methods=['POST'])
def upload_file():
    # TODO:
    if 'file' not in request.files:
        return jsonify({'Error': 'No file provided'}), 400
    
    file = request.files['file']

    # normalization method check
    normalization = request.form.get('normalization', "none").lower()
    if normalization not in ALLOWED_NORMALIZATIONS:
        return jsonify({'Error': f'Invalid normalization method: {normalization}'}), 400

    # Check if the file is a txt file
    if file and file.filename.lower().endswith('.txt'):
        filename = f"{uuid.uuid4().hex}.txt"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # === 关键调试：打印/返回真实路径与目录现状 ===
        app.logger.info(f"BASE_DIR={os.path.dirname(os.path.abspath(__file__))}")
        app.logger.info(f"UPLOAD_FOLDER={app.config['UPLOAD_FOLDER']}")
        app.logger.info(f"RESULT_FOLDER={app.config['RESULT_FOLDER']}")
        app.logger.info(f"Saved file path={save_path}")
        app.logger.info(f"Uploads dir content={os.listdir(app.config['UPLOAD_FOLDER'])}")
    else:
        return jsonify({'error': 'Only txt files are allowed'}), 400
 
    try:
        result_files = run_all_r_scripts(
            save_path,
            normalization,
            app.config['RESULT_FOLDER']
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "normalization": normalization,
        "results": result_files
    }), 200

if __name__ == '__main__':
    app.run(debug=True)