from flask import Blueprint
from controllers.studenti_controller import *

studenti_bp = Blueprint("studenti", __name__)

studenti_bp.route("/", methods=["GET"])(get_studenti)
studenti_bp.route("/<id>", methods=["GET"])(get_studente)
studenti_bp.route("/", methods=["POST"])(create_studente)
studenti_bp.route("/<id>", methods=["PUT"])(update_studente)
studenti_bp.route("/<id>", methods=["DELETE"])(delete_studente)

studenti_bp.route("/iscrivi", methods=["POST"])(iscrivi_studente)
