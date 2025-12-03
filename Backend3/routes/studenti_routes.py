from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId

studenti_bp = Blueprint("studenti_bp", __name__)

# ===========================
#  GET tutti gli studenti
# ===========================
@studenti_bp.get("/")
def route_get_studenti():
    mongo = current_app.mongo
    studenti = []
    for s in mongo.studenti.find():
        s["_id"] = str(s["_id"])
        studenti.append(s)
    return jsonify(studenti), 200

# ===========================
#  GET studente singolo
# ===========================
@studenti_bp.get("/<id>")
def route_get_studente(id):
    mongo = current_app.mongo
    try:
        studente = mongo.studenti.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if not studente:
        return jsonify({"error": "Studente non trovato"}), 404

    studente["_id"] = str(studente["_id"])
    return jsonify(studente), 200

# ===========================
#  POST crea nuovo studente
# ===========================
@studenti_bp.post("/")
def route_create_studente():
    mongo = current_app.mongo
    data = request.json

    # Documento studente
    studente = {
        "nome": data["nome"],
        "cognome": data.get("cognome", ""),
        "email": data.get("email", ""),
        "moduli_iscritti": []  # lista di ID moduli
    }

    nuovo_id = mongo.studenti.insert_one(studente).inserted_id
    return jsonify({"_id": str(nuovo_id)}), 201

# ===========================
#  PUT aggiorna studente
# ===========================
@studenti_bp.put("/<id>")
def route_update_studente(id):
    mongo = current_app.mongo
    data = request.json

    update = {
        "nome": data.get("nome"),
        "cognome": data.get("cognome"),
        "email": data.get("email"),
        "telefono": data.get("telefono"),
    }

    # Rimuove i campi None
    update = {k: v for k, v in update.items() if v is not None}

    try:
        result = mongo.studenti.update_one({"_id": ObjectId(id)}, {"$set": update})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if result.matched_count == 0:
        return jsonify({"error": "Studente non trovato"}), 404

    return jsonify({"message": "Studente aggiornato"}), 200

# ===========================
#  DELETE studente
# ===========================
@studenti_bp.delete("/<id>")
def route_delete_studente(id):
    mongo = current_app.mongo
    try:
        result = mongo.studenti.delete_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "Studente non trovato"}), 404

    return jsonify({"message": "Studente eliminato"}), 200
