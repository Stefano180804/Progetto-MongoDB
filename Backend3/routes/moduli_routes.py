# routes/moduli_routes.py
from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId  # per convertire _id di Mongo

moduli_bp = Blueprint("moduli_bp", __name__)

# ------------------------------
# GET tutti i moduli
# ------------------------------
@moduli_bp.get("/")
def route_get_moduli():
    mongo = current_app.mongo  # Prende il client MongoDB dall'app
    moduli = []
    for m in mongo.moduli.find():
        m["_id"] = str(m["_id"])
        moduli.append(m)
    return jsonify(moduli), 200

# ------------------------------
# GET modulo singolo per ID
# ------------------------------
@moduli_bp.get("/<id>")
def route_get_modulo(id):
    mongo = current_app.mongo
    try:
        modulo = mongo.moduli.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if not modulo:
        return jsonify({"error": "Modulo non trovato"}), 404
    modulo["_id"] = str(modulo["_id"])
    return jsonify(modulo), 200

# ------------------------------
# POST crea nuovo modulo
# ------------------------------
@moduli_bp.post("/")
def route_create_modulo():
    mongo = current_app.mongo
    data = request.json
    # Creazione documento modulo completo
    modulo = {
        "nome": data["nome"],
        "codice": data.get("codice", ""),
        "ore_totali": data.get("ore_totali", 0),
        "descrizione": data.get("descrizione", ""),
        "studenti_iscritti": []
    }
    nuovo_id = mongo.moduli.insert_one(modulo).inserted_id
    return jsonify({"_id": str(nuovo_id)}), 201

# ------------------------------
# PUT aggiorna modulo esistente
# ------------------------------
@moduli_bp.put("/<id>")
def route_update_modulo(id):
    mongo = current_app.mongo
    data = request.json
    update = {
        "nome": data.get("nome"),
        "codice": data.get("codice"),
        "ore_totali": data.get("ore_totali"),
        "descrizione": data.get("descrizione")
    }
    update = {k: v for k, v in update.items() if v is not None}

    try:
        result = mongo.moduli.update_one({"_id": ObjectId(id)}, {"$set": update})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if result.matched_count == 0:
        return jsonify({"error": "Modulo non trovato"}), 404
    return jsonify({"message": "Modulo aggiornato"}), 200

# ------------------------------
# DELETE modulo
# ------------------------------
@moduli_bp.delete("/<id>")
def route_delete_modulo(id):
    mongo = current_app.mongo
    try:
        result = mongo.moduli.delete_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "ID non valido"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "Modulo non trovato"}), 404
    return jsonify({"message": "Modulo eliminato"}), 200
