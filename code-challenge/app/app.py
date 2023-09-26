#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Hero, Power

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

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)

    if hero is None:
        return make_response(jsonify({"error": "Hero not found"}), 404)

    # Get powers associated with the hero
    powers = []
    for hero_power in hero.powers:
        power = Power.query.get(hero_power.power_id)
        powers.append({
            "id": power.id,
            "name": power.name,
            "description": power.description
        })

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers
    }

    return jsonify(hero_data)


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [
        {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        for power in powers
    ]
    return jsonify(powers_data)


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)

    if power is None:
        return make_response(jsonify({"error": "Power not found"}), 404)

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return jsonify(power_data)


if __name__ == '__main__':
    app.run(port=5555)
