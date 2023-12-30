from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fav_planets = db.relationship('FavoritePlanets', backref='fav_planets_id')
    fav_people = db.relationship('FavoritePeople', backref='fav_people_id')
    fav_starships = db.relationship('FavoriteStarships', backref='fav_starships_id')
  
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
            }
    

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(100),  unique=True, nullable=False)
    planet_diameter = db.Column(db.Integer, unique=True, nullable=False)
   
    def __repr__(self):
        return '<Planets %r>' % self.planet_name

    def serialize(self):
        return {
            'id': self.id,
            'planet_name': self.planet_name,
            'planet_size': self.planet_diameter,
        }

    
class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fav_planets = db.Column(db.Integer, db.ForeignKey('planets.id'),primary_key=True)

    def __repr__(self):
        return '<FavoritePlanets %r>' % self.fav_planets


    def serialize(self):
        return {
            'id': self.id,
            'fav_planets': self.fav_planets,
        }

class People(db.Model): 
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(100), unique=True, nullable=False) 
    birth_year = db.Column (db.Integer,  unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.person_name

    def serialize(self):
        return {
            'id': self.id,
            'person_name': self.person_name,
            'birth_year': self.birth_year, 
        }
    
class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fav_people = db.Column(db.Integer, db.ForeignKey('people.id'),primary_key=True)


    def __repr__(self):
        return '<FavoritePeople %r>' % self.fav_people
    
    def serialize(self):
        return {
            'id': self.id,
            'fav_people': self.fav_people,
        
        }
    

class Starships (db.Model): 
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    starship_name = db.Column (db.String(100), unique=True, nullable=False) 
    starship_model = db.Column (db.String(), unique=True, nullable=False)

    def __repr__(self):
        return '<Starships %r>' % self.starship_name

    def serialize(self):
        return {
            'id': self.id,
            'starship_name': self.starship_name,
            'starship_model': self.starship_model,
        
        }

class FavoriteStarships(db.Model):
    __tablename__ = 'favorite_starships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fav_starships = db.Column(db.Integer, db.ForeignKey('starships.id'),primary_key=True)

    def __repr__(self):
        return '<FavoriteStarships %r>' % self.fav_starships
    
    def serialize(self):
        return {
            'id': self.id,
            'fav_starships': self.fav_starships, 
        
        }
