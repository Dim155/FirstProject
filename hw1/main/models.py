from hw1.main.database import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    credit_card = db.Column(db.String(16))
    car_number = db.Column(db.String(10), unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'credit_card': self.credit_card,
            'car_number': self.car_number
        }

class Parking(db.Model):
    __tablename__ = 'parkings'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)
    opened = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'count_places': self.count_places,
            'count_available_places': self.count_available_places,
            'opened': self.opened
        }

class ClientParking(db.Model):
    __tablename__ = 'client_parkings'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship('Client')
    parking = db.relationship('Parking')
