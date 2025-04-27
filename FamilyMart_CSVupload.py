from flask import Flask
import requests

app = Flask(__name__)

upload_url = 'https://familymartcsv.onrender.com/upload'
local_file = r'C:\Users\vincent.hung\Desktop\FamilyMart\API\sample.csv'

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
        with open(local_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(upload_url, files=files)
        return response.text
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
