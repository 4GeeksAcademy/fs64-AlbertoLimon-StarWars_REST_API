"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['GET'])
def get_all_users():
    
    users = User.query.all()
    users = list(map(lambda user: user.to_dict(), users))

    return jsonify({
        "data": users
    }), 200

@app.route('/user', methods=['POST'])
def create_user():

    user = User()
    data = request.get_json()
    user.name = data["name"]
    user.username = data["username"]
    user.password = data["password"]

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "user created"
    }), 200

@app.route('/user/<int:id>', methods=['GET','PUT','DELETE'])
def handle_user(id):

    if request.method == 'GET':
    
        user = User.query.get(id)
        data = user.to_dict()

        return data, 200
    
    elif request.method == 'PUT':
        user = User.query.get(id)
        if user is not None:
            data = request.get_json()
            user.username = data["username"]
            db.session.commit()
            return jsonify({
                "msg":"user updated"
            }),200
        else:
            return jsonify({
                "msg": "user not found"
            }), 404
        
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

            return jsonify({
                "msg":"user deleted"
            }),202
        else:
            return jsonify({
                "msg":"user not found"
            }), 404
        
    


@app.route('/character', methods=['GET'])
def get_all_characters():
   
        characters = Character.query.all()
        return jsonify([character.name for character in characters]), 200
    
@app.route('/character', methods=['POST'])
def create_character():

    
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "character created"
        }), 200

@app.route('/character/<int:id>', methods=['GET','PUT','DELETE'])
def handle_character(id):
    if request.method == 'GET':
        
        character = Character.query.get(id)
        

        return jsonify(character.serialize()), 200
    
    elif request.method == 'PUT':
        character = Character.query.get(id)
        if character is not None:
            data = request.get_json()
            character.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"character updated"
            }),200
        else:
            return jsonify({
                "msg": "character not found"
            }), 404
        
    elif request.method == 'DELETE':
        character = Character.query.get(id)
        if character is not None:
            db.session.delete(character)
            db.session.commit()

            return jsonify({
                "msg":"character deleted"
            }),202
        else:
            return jsonify({
                "msg":"character not found"
            }), 404
    
    

@app.route('/planet', methods=['GET'])
def get_all_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.to_dict(), planets))

        return jsonify({
            "data": planets
        }), 200

@app.route('/planet', methods=['GET'])
def create_planet():
     if request.method == 'POST':
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]

        db.session.add(planet)
        db.session.commit()

        return jsonify({
            "msg": "planet created"
        }), 200
    
@app.route("/planet/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def handle_planet(id):

    if request.method == 'GET':
       
        planet = Planet.query.get(id)
        
        return jsonify(planet.serialize()), 200

    elif request.method == 'PUT':
        planet = Planet.query.get(id)
        if planet is not None:
            data = request.get_json()
            planet.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"planet updated"
            }),200
        else:
            return jsonify({
                "msg": "planet not found"
            }), 404
        
    elif request.method == 'DELETE':
        planet = Planet.query.get(id)
        if planet is not None:
            db.session.delete(planet)
            db.session.commit()

            return jsonify({
                "msg":"planet deleted"
            }),202
        else:
            return jsonify({
                "msg":"planet not found"
            }), 404


@app.route('/user/<int:id>/favorite', methods=['GET'])
def handle_favorite(id):
    user_id = id
    favorites = Favorite.query.filter_by(user_id=user_id)
    favorites = list(map(lambda favorite: favorite.to_dict(), favorites))

    return jsonify({
        "data": favorites
    }), 200

@app.route('/favorite', methods=['POST'])
def create_favorite():
    
    favorite = Favorite()
    data = request.get_json()
    user_id = data["user_id"]

    if data["character_id"] is None:
        character_id = "0"
    character_id = data["character_id"]
    if data["planet_id"] is None:
        planet_id = "0"
    planet_id = data["planet_id"]
    
    user_filter = User.query.filter_by(id=user_id)
    character_filter = Character.query.filter_by(id=character_id)
    planet_filter = Planet.query.filter_by(id=planet_id)

    if user_filter is not None and character_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_character = data["character_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    elif user_filter is not None and planet_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_planet = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    else:
        return jsonify({
                "msg":"favorite could not be create, make sure user, character or planet exists"
            }), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
