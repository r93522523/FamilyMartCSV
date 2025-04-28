from flask import Flask, jsonify
import csv
import json
import requests
import os
import shutil
from base64 import b64encode
from pathlib import Path

print("Current working directory:", os.getcwd())
print("Target file exists:", os.path.exists("/opt/render/project/src/sample.csv"))

app = Flask(__name__)

csv_path = os.path.abspath("/opt/render/project/src/sample.csv")

BATCH_SIZE = 2

def csv_to_json(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        batch = []
        for row in reader:
            item = {
                "itemId": row.get("BARCODE", "").strip(),
                "itemName": row.get("CMNM", "").strip(),
                "price": row.get("SLUNT", "").strip(),
                "properties": {
                    "CMBND": row.get("CMBND", "").strip(),
                    "SPC": row.get("SPC", "").strip(),
                    "Promo_id": row.get("Promo_id", "").strip(),
                    "Promo_text": row.get("Promo_text", "").strip(),
                    "Foodsafety": row.get("Foodsafety", "").strip(),
                    "FU_SPACE": row.get("FU_SPACE", "").strip()
                }
            }
            batch.append(item)
            if len(batch) == BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch

tokenurl = "https://central-manager.familymart-tw-test.pcm.pricer-plaza.com/api/public/auth/v1/login"
apitoken = requests.get(tokenurl , auth=('api@familymart.com.tw','Api@familymart2025'))
token = apitoken.text[28:-2]
head = {"Authorization":"Bearer " + token, "Content-Type":"application/json"}

update_url = "https://apitest.familymart-tw-test.pcm.pricer-plaza.com/api/public/core/v1/items"

@app.route('/run-job', methods=['POST'])
def run_job():
    if not os.path.exists(csv_path):
        return jsonify({"status": "error", "message": f"找不到檔案: {csv_path}"}), 404

    results = []
    for batch in csv_to_json(csv_path):
        response = requests.patch(update_url , json=batch, headers=head)
        results.append(batch)

    return jsonify({"status": "success", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
