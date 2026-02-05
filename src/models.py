from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    favorites=db.relationship("Favorite", uselist=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(50))
    species = db.Column(db.String(50))

    favorites = db.relationship('Favorite', backref='character', lazy=True)

    def serialize(self):
        return {
            "Character": self.name,
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))

    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    user= db.relationship("User",back_populates="favorites")

    def __repr__(self):
        return f'<Favorite user={self.user_id}>'