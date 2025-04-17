from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open("seriais.json", "r") as f:
    seriais = json.load(f)

@app.route("/validar", methods=["GET"])
def validar_serial():
    serial = request.args.get("serial")
    dispositivo_id = request.args.get("android_id")

    if serial in seriais:
        dados = seriais[serial]
        if dados["usado"] and dados["dispositivo_id"] != dispositivo_id:
            return jsonify({"autorizado": False, "mensagem": "Serial já usado em outro dispositivo"})
        else:
            dados["usado"] = True
            dados["dispositivo_id"] = dispositivo_id
            with open("seriais.json", "w") as f:
                json.dump(seriais, f)
            return jsonify({"autorizado": True, "mensagem": "Serial válido!"})
    return jsonify({"autorizado": False, "mensagem": "Serial inválido"})
