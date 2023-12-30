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
from models import db, User, People, Planets, Starships, FavoritePlanets,FavoritePeople, FavoriteStarships
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

@app.route('/users', methods=['GET'])
def handle_user():
    users = User.query.all()
    data = [user.serialize() for user in users]

    return jsonify(data), 200

@app.route('/users/favoriteplanets/<int:user_id>', methods=['GET'])
def handle_get_users_favorite_planets(user_id):
    fav_planets = FavoritePlanets.query.filter_by(user_id == user_id)

    return jsonify(fav_planets), 200

@app.route ('/planets', methods=['GET'])
def get_list_planets():
    planets_list = Planets.query.all()
    data = [planet.serialize() for planet in planets_list]
    return jsonify(data), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_get_one_planet(planet_id):
    one_planet = Planets.query.get(planet_id)

    if one_planet is None:
        return jsonify({"error": "The planet you look for is not found"}), 404

    return jsonify(one_planet), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_new_favorite_planet(planet_id):
    data = request.json
    favPlanets = FavoritePlanets(user_id= data.get('user_id'), fav_planets= planet_id)
    db.session.add(favPlanets)
    db.session.commit()
    return jsonify({"msg": "new favorite planet added"})

@app.route('/users/favoritepeople/<int:user_id>', methods=['GET'])
def handle_get_users_favorite_people(user_id):
    fav_planets = FavoritePlanets.query.filter_by(user_id=user_id)
    return jsonify(fav_planets), 200


@app.route ('/people', methods=['GET'])
def get_list_people():
    people_list = People.query.all()
    data = [people.serialize() for people in people_list]
    return jsonify(data), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_get_single_people(people_id):
    single_people = People.guery.get(people_id)

    if single_people is None:
        return jsonify({"error": "One single people not found"}), 404

    return jsonify(single_people), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_new_favorite_people():
    data = request.json
    favPeople = FavoritePeople(user_id= data.get('user_id'), fav_people= people_id) 
    db.session.add(favPeople)
    db.session.commit()
    return jsonify({"msg": "new favorite people added"})


@app.route('/users/favoritestarships/<int:user_id>', methods=['GET'])
def handle_get_users_favorite_starships(user_id):
    fav_starships = FavoriteStarships.query.filter_by(user_id == user_id)

    return jsonify(fav_starships), 200

@app.route ('/starships', methods=['GET'])
def get_list_starships():
    starships_list = Starships.query.all()
    data = [starships.serialize() for starships in starships_list]
    return jsonify(data), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def handle_get_one_starship(starship_id):
    one_starship = Starships.query.get(starship_id)

    if one_starship is None:
        return jsonify({"error": "The starship you look for is not found"}), 404

    return jsonify(one_starship), 200

@app.route('/favorite/starships/<int:starship_id>', methods=['POST'])
def handle_new_favorite_starship():
    data = request.json
    favStarships = FavoriteStarships(user_id= data.get('user_id'), fav_starships= starship_id)
    db.session.add(favStarships)
    db.session.commit()
    return jsonify({"msg": "new favorite starship added"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
