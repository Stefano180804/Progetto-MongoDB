from flask import request, jsonify
from bson.objectid import ObjectId
from config import mongo

def get_studenti():
    studenti = list(mongo.db.studenti.find())
    for s in studenti:
        s["_id"] = str(s["_id"])
        s["moduli_iscritti"] = [str(m) for m in s.get("moduli_iscritti", [])]
    return jsonify(studenti)

def get_studente(id):
    studente = mongo.db.studenti.find_one({"_id": ObjectId(id)})
    if not studente:
        return jsonify({"error": "Studente non trovato"}), 404

    studente["_id"] = str(studente["_id"])
    studente["moduli_iscritti"] = [str(m) for m in studente.get("moduli_iscritti", [])]
    return jsonify(studente)

def create_studente():
    data = request.json
    nuovo_id = mongo.db.studenti.insert_one({
        "nome": data["nome"],
        "cognome": data["cognome"],
        "email": data["email"],
        "moduli_iscritti": []
    }).inserted_id
    return jsonify({"_id": str(nuovo_id)}), 201

def update_studente(id):
    data = request.json
    mongo.db.studenti.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Studente aggiornato"})

def delete_studente(id):
    mongo.db.studenti.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Studente eliminato"})


# Endpoint per iscrivere uno studente a un modulo
def iscrivi_studente():
    data = request.json
    studente_id = ObjectId(data["studenteId"])
    modulo_id = ObjectId(data["moduloId"])

    # Aggiorna studente
    mongo.db.studenti.update_one(
        {"_id": studente_id},
        {"$addToSet": {"moduli_iscritti": modulo_id}}
    )

    # Aggiorna modulo
    mongo.db.moduli.update_one(
        {"_id": modulo_id},
        {"$addToSet": {"studenti_iscritti": studente_id}}
    )

    return jsonify({"message": "Studente iscritto al modulo"})
