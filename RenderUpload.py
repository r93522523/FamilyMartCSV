from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        save_path = os.path.join('/mnt/data', file.filename)
        file.save(save_path)
        return f'File saved to {save_path}'

if __name__ == "__main__":
    app.run()
