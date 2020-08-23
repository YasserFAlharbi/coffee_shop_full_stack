import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
# Done uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

# Done implement endpoint GET /drinks
# public endpoint that contain only the drink.short() data representation
# Returns status code 200 and json or appropriate status code indicating reason for failure
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        all_drinks = Drink.query.order_by(Drink.id).all()
        if not all_drinks:
            abort(400)

        drinks = [drink.short() for drink in all_drinks]
        
        return jsonify({
            'success':True,
            'drinks': drinks
        }), 200

    except Exception as error:
        raise error


# Done implement endpoint GET /drinks-detail
# Require Permission('get:drinks-detail') that contain the drink.long() data representation
# Returns status code 200 and a list of drinks in json format or appropriate status code indicating reason for failure
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details(jwt):
    try:
        all_drinks = Drink.query.all()
        if not all_drinks:
            abort(400)

        drinks = [drink.long() for drink in all_drinks]

        return jsonify({
            'success':True,
            'drinks': drinks
        }), 200

    except Exception as error:
        raise error


# Done implement endpoint POST /drinks to create a new drink in the database
# Require Permission('post:drinks') that contain the drink.long() data representation for new drink
# Returns status code 200 and json {"success": True, "drinks": drink} where drink an array 
# containing only the newly created drink or appropriate status code indicating reason for failure    
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    try:
        new_drink = request.get_json()

        title = json.loads(request.data)['title']

        if title == '':
            abort(400)

        drink = Drink(
            title=new_drink.get('title'),
            recipe=json.dumps(new_drink.get('recipe'))
        )

        drink.insert()

        return jsonify({
            'success':True,
            'drink': drink.long()
        }), 200

    except Exception as error:
        raise error


# Done implement endpoint PATCH /drinks/<id> to update the corresponding row for <id>
# It will respond with a 404 error if <id> is not found
# Require the 'patch:drinks' permission that contain the drink.long() data representation for updated drink
# Returns status code 200 and json {"success": True, "drinks": drink} where drink
# an array containing only the updated drink or appropriate status code indicating reason for failure
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        request_body = request.get_json()

        if not drink:
            abort(404)
        
        title = json.loads(request.data)['title']

        if title == '':
            abort(400)
        
        drink.title = title

        if 'recipe' in request_body:
            recipe = json.loads(request.data)['recipe']
            drink.recipe = json.dumps(recipe)
        
        drink.update()

        return jsonify({
            'success':True,
            'drinks': drink.long()
        }), 200

    except Exception as error:
        raise error
    

# Done implement endpoint DELETE /drinks/<id> to delete the corresponding row for <id>
# It will respond with a 404 error if <id> is not found
# Require the 'delete:drinks' permission
# Returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if not drink:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    except Exception as error:
        raise error


## Error Handling

# error handling for unprocessable entity
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
    "success": False, 
    "error": 422,
    "message": "unprocessable"
    }), 422


# Done implement error handlers for bad request
@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
    "success": False, 
    "error": 400,
    "message": "bad request"
    }), 400


# Done implement error handlers for resource not found
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
    "success": False, 
    "error": 404,
    "message": "resource not found"
    }), 404


# Done implement error handlers for AuthError
@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
    "success": False, 
    "error": 401,
    "message": "Authorization error"
    }), 401

# Done implement error handlers for server error
@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
    "success": False, 
    "error": 500,
    "message": "Internal Server Error"
    }), 500
