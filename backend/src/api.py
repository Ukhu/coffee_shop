import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

## db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        abort(422)

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        abort(422)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title is None or recipe is None:
        abort(400)

    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        created_drink = Drink.query.filter_by(title=title).one_or_none()

        return jsonify({
            'success': True,
            'drinks': [created_drink.long()]
        }), 201

    except:
        print(sys.exc_info())
        abort(422)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        error = None

        drink = Drink.query.filter_by(id=id).one_or_none()
        
        if drink is None:
            error = 404
            abort(404)
        
        if title is None and recipe is None:
            error = 400
            abort(400)

        if title is None:
            drink.recipe = json.dumps(recipe)
            drink.update()
        elif recipe is None:
            drink.title = title
            drink.update()
        else:
            drink.title = title
            drink.recipe =  json.dumps(recipe)
            drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except:
        if error == 404:
            abort(404)
        if error == 400:
            abort(400)
        print(sys.exc_info())
        abort(422)

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).one_or_none()
        
        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink.id
        })

    except:
        abort(422)


## Error Handling

@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'success':False,
        'status':400,
        'message':'bad request'
    }), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success':False,
        'status':404,
        'message':'resource not found'
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        'success':False,
        'status': e.status_code,
        'message': e.error['description']
    }), e.status_code
