from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }
    
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_character = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user = db.relationship(User)

    def to_dict(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "user_character": self.user_character,
            "user_planet": self.user_planet
        }
    