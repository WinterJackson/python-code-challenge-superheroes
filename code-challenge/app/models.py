from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy.orm import validates


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    super_name = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    powers = db.relationship('HeroPower', back_populates='hero')

    def __repr__(self):
        return f"<Hero: {self.name}, {self.super_name}>"

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    heroes = db.relationship('HeroPower', back_populates='power')

    # Validation for description
    @validates('description')
    def validate_description(self, value):
        if not value:
            raise ValueError('Description must be present')
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return value


    def __repr__(self):
        return f"<Power: {self.name}, {self.description}>"

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String(255))
    
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    # Validation for strength
    @validates('strength')
    def validate_strength(self, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError('Strength must be one of: Strong, Weak, Average')
        return value

    def __repr__(self):
        return f"<{self.hero_id}, HeroPower: {self.power_id}, {self.strength}>"