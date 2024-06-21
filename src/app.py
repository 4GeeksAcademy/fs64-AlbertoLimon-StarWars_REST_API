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

@app.route('/user', methods=['GET','PUT','DELETE'])
def handle_user():

    if request.method == 'GET':
        user_id = id
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
    if request.method == 'GET':
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))

        return jsonify({
            "data": characters
        }), 200

@app.route('/character', methods=['GET'])
def get_single_characters():
     if request.method == 'GET':
        
        character = Character.query.get(id)
        data = character.to_dict()

        return data, 200
    
@app.route('/character', methods=['GET'])
def create_character():

    if request.method == 'POST':
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "character created"
        }), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    if request.method == 'GET':
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))

        return jsonify({
            "data": characters
        }), 200

@app.route('/character', methods=['GET'])
def get_single_characters():
     if request.method == 'GET':
        
        character = Character.query.get(id)
        data = character.to_dict()

        return data, 200
    
@app.route('/character', methods=['GET'])
def create_character():

    if request.method == 'POST':
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "character created"
        }), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
