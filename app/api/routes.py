from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Drink, db, User, Drink, drink_schema, drinks_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata', methods=['GET'])
def getdata():
    return {'some':'JSON'}

@api.route('/drinks', methods = ['POST'])
@token_required
def create_drink(current_user_token):
    name = request.json['name']
    description = request.json['description']
    type = request.json['type']
    stocks = request.json['stocks']
    sugar= request.json['sugar']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    drink = Drink (name, description, type ,stocks,sugar, user_token = user_token )

    db.session.add(drink)     
    db.session.commit()

    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drink(current_user_token):
    a_user = current_user_token.token
    drinks = Drink.query.filter_by(user_token = a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)    


@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    drink = Drink.query.get(id)
    response = drink_schema.dump(drink)
    return jsonify(response) 

@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    drink = Drink.query.get(id) 
    drink.name = request.json['name']
    drink.description = request.json['description']
    drink.type = request.json['type']
    drink.stocks = request.json['stocks']
    drink.sugar = request.json['sugar']
    drink.user_token = current_user_token.token

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)  


@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)        