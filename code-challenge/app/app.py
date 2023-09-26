#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h2>Welcome!<h2>'

@app.route('/heroes', methods=['GET'])
def get_heroes():

    heroes = Hero.query.all()
    heroes_data = [
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(heroes_data)


if __name__ == '__main__':
    app.run(port=5555)
