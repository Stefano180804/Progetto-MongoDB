from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

from routes.moduli_routes import moduli_bp
from routes.studenti_routes import studenti_bp

def create_app():
    app = Flask(__name__)

    # Abilita CORS (utile se hai un frontend separato)
    CORS(app)

    # -----------------------------
    # Connessione al database (PyMongo)
    # -----------------------------
    client = MongoClient("mongodb://localhost:27017/")  # Connessione locale
    app.mongo = client.gestione_corsi_its  # "miodb" è il nome del tuo DB

    # Registrazione delle rotte
    app.register_blueprint(moduli_bp, url_prefix="/moduli")
    app.register_blueprint(studenti_bp, url_prefix="/studenti")

    return app

# CREA L'APP
app = create_app()

# Stampa le rotte registrate per debug
print(app.url_map)

# Avvio dell'app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
