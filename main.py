import os
from flask import Flask, jsonify

# Létrehozzuk a Flask alkalmazás példányát
app = Flask(__name__)

# A portot környezeti változóból olvassuk be,
# de ha nincs beállítva, alapértelmezetten 8080-at használunk.
PORT = int(os.environ.get('PORT', 8080))

# A feladat által kért szabadon választott string, ami a HTTP válaszban szerepel
STATUS_MESSAGE = "GDE B-DEVOPS beadandó KÉSZ"
EXPECTED_STATUS_CODE = 200

@app.route('/status', methods=['GET'])
def status():
    """
    Egy egyszerű HTTP végpont, amely visszaadja az alkalmazás állapotát és a kért stringet.
    """
    # A HTTP válasz sikeres (200 OK) és tartalmazza a tetszőleges stringet
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
    # Flask alkalmazás indítása, a megadott porton és bármely elérhető címen (0.0.0.0)
    # Fontos a 0.0.0.0, mert a Docker konténerben is ezen kell figyelnie.
    print(f"Flask app is running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT)