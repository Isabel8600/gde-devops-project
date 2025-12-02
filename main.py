import os
from flask import Flask, jsonify

# Létrehozzuk a Flask alkalmazás példányát
app = Flask(__name__)

PORT = int(os.environ.get('PORT', 8080))

STATUS_MESSAGE = "GDE B-DEVOPS beadandó KÉSZ"
EXPECTED_STATUS_CODE = 200

@app.route('/status', methods=['GET'])
def status():
    """
    Egy egyszerű HTTP végpont, amely visszaadja az alkalmazás állapotát és a kért stringet.
    """
    response_data = {
        "status": "OK",
        "message": STATUS_MESSAGE,
        "api_version": "1.0"
    }
    return jsonify(response_data), EXPECTED_STATUS_CODE

@app.route('/', methods=['GET'])
def home():
    """
    Kezdőoldali végpont.
    """
    return jsonify({"info": "Használd a /status végpontot az állapot lekéréséhez."}), EXPECTED_STATUS_CODE

if __name__ == '__main__':
    print(f"Flask app is running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT)