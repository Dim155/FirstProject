from datetime import datetime

from flask import Flask, jsonify, request

from hw1.main.database import db
from hw1.main.models import Client, ClientParking, Parking


class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.get_json()
        new_client = Client(**data)
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_json()), 201

    @app.route("/clients", methods=["GET"])
    def list_clients():
        clients = Client.query.all()
        return jsonify([client.to_json() for client in clients]), 200

    @app.route("/clients/<int:id>", methods=["GET"])
    def get_client(id):
        client = Client.query.get_or_404(id)
        return jsonify(client.to_json()), 200

    @app.route("/clients/<int:id>", methods=["PUT"])
    def update_client(id):
        data = request.get_json()
        client = Client.query.get_or_404(id)
        for key, value in data.items():
            setattr(client, key, value)
        db.session.commit()
        return jsonify(client.to_json()), 200

    @app.route("/clients/<int:id>", methods=["DELETE"])
    def delete_client(id):
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return "", 204

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.get_json()
        new_parking = Parking(**data)
        db.session.add(new_parking)
        db.session.commit()
        return jsonify(new_parking.to_dict()), 201

    @app.route("/parkings", methods=["GET"])
    def list_parkings():
        parkings = Parking.query.all()
        return jsonify([parking.to_dict() for parking in parkings]), 200

    @app.route("/parkings/<int:id>", methods=["GET"])
    def get_parking(id):
        parking = Parking.query.get_or_404(id)
        return jsonify(parking.to_dict()), 200

    @app.route("/client_parkings", methods=["POST"])
    def enter_parking():
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        parking = Parking.query.get_or_404(parking_id)
        if parking.count_available_places <= 0:
            return jsonify({"message": "Парковка заполнена"}), 404

        new_entry = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.now()
        )
        db.session.add(new_entry)
        parking.count_available_places -= 1
        if parking.count_available_places == 0:
            parking.opened = False
        db.session.commit()
        return jsonify({"message": "Автомобиль успешно поставлен на парковку."}), 201

    @app.route("/client_parkings", methods=["DELETE"])
    def leave_parking():
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        client_parking = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id
        ).first()
        if not client_parking:
            return jsonify({"message": "Запись не найдена"}), 404

        parking = Parking.query.get_or_404(parking_id)
        client_parking.time_out = datetime.now()
        parking.count_available_places += 1
        if parking.count_available_places > 0:
            parking.opened = True
        db.session.commit()
        return jsonify({"message": "Автомобиль успешно покинул парковку."}), 200

    return app
