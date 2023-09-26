#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

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

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)

    if power is None:
        return make_response(jsonify({"error": "Power not found"}), 404)

    request_data = request.get_json()

    if 'description' not in request_data:
        return make_response(jsonify({"errors": ["Description is required"]}), 400)

    new_description = request_data['description']
    power.description = new_description

    # Validate the power model
    errors = power.validate()
    if errors:
        return make_response(jsonify({"errors": errors}), 400)

    db.session.commit()

    updated_power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return jsonify(updated_power_data)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():

    request_data = request.get_json()

    required_fields = ["strength", "power_id", "hero_id"]
    for field in required_fields:
        if field not in request_data:
            return make_response(jsonify({"errors": [f"{field} is required"]}), 400)

    strength = request_data['strength']
    power_id = request_data['power_id']
    hero_id = request_data['hero_id']

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if power is None or hero is None:
        return make_response(jsonify({"errors": ["Power or Hero not found"]}), 404)

    hero_power = HeroPower(strength=strength, power=power, hero=hero)

    errors = hero_power.validate()
    if errors:
        return make_response(jsonify({"errors": errors}), 400)

    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description
            }
            for p in hero.powers
        ]
    }

    return jsonify(hero_data)


if __name__ == '__main__':
    app.run(port=5555)
