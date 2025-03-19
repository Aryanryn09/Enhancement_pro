from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os  # For environment variables

app = Flask(__name__)  # ✅ Corrected double underscore
CORS(app)  # Allow frontend to communicate with backend

# Load Cloudflare credentials from environment variables
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")


def call_cloudflare_ai(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"prompt": prompt}

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            return response.json().get("result", {}).get("response", "Error: No response found")
        except Exception as e:
            return f"JSON Parsing Error: {str(e)}"
    else:
        return f"API Error: {response.text}"

@app.route('/improve-resume', methods=['POST'])
def improve_resume():
    data = request.json
    prompt = (
        f"Improve this resume section:\n\n"
        f"Summary: {data.get('summary', 'N/A')}\n"
        f"Education: {data.get('education', 'N/A')}\n"
        f"Skills: {data.get('skills', 'N/A')}\n"
        f"Projects: {data.get('projects', 'N/A')}\n"
        f"Experience: {data.get('experience', 'N/A')}\n"
        f"Extra Curricular: {data.get('extra', 'N/A')}"
    )

    improved_text = call_cloudflare_ai(prompt)
    
    return jsonify({"improved_resume": improved_text})

if __name__ == '__main__':  # ✅ Corrected double underscore
    app.run(debug=True)
