from flask import request, jsonify
from bson.objectid import ObjectId
from config import mongo

def get_moduli():
    moduli = list(mongo.db.moduli.find())
    for m in moduli:
        m["_id"] = str(m["_id"])
        m["studenti_iscritti"] = [str(s) for s in m.get("studenti_iscritti", [])]
    return jsonify(moduli)

def get_modulo(id):
    modulo = mongo.db.moduli.find_one({"_id": ObjectId(id)})
    if not modulo:
        return jsonify({"error": "Modulo non trovato"}), 404

    modulo["_id"] = str(modulo["_id"])
    modulo["studenti_iscritti"] = [str(s) for s in modulo.get("studenti_iscritti", [])]
    return jsonify(modulo)

def create_modulo():
    data = request.json
    nuovo_id = mongo.db.moduli.insert_one({
        "nome": data["nome"],
        "codice": data.get("codice", ""),
        "ore_totali": data.get("ore_totali", 0),
        "descrizione": data.get("descrizione", ""),
        "studenti_iscritti": []
    }).inserted_id
    return jsonify({"_id": str(nuovo_id)}), 201

def update_modulo(id):
    data = request.json
    mongo.db.moduli.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Modulo aggiornato"})

def delete_modulo(id):
    mongo.db.moduli.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Modulo eliminato"})
