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
        # get all drinks from database
        all_drinks = Drink.query.order_by(Drink.id).all()
        # check if no data in drink table abort with status code 400
        if not all_drinks:
            abort(400)
        # get the drinks list
        drinks = [drink.short() for drink in all_drinks]
        
        return jsonify({
            'success':True,
            'drinks': drinks
        }), 200

    except Exception as error:
        # raise appropriate status code reflecting the reason of failure
        raise error


# Done implement endpoint GET /drinks-detail
# Require Permission('get:drinks-detail') that contain the drink.long() data representation
# Returns status code 200 and a list of drinks in json format or appropriate status code indicating reason for failure

@app.route('/drinks-detail')
# use of requires_auth decorator to check permission 'get:drinks-detail'
@requires_auth('get:drinks-detail')
def get_drink_details(jwt):
    try:
        # get all drinks from database
        all_drinks = Drink.query.all()
        # check if no data in drink table abort with status code 400
        if not all_drinks:
            abort(400)
        # get the drinks list
        drinks = [drink.long() for drink in all_drinks]

        return jsonify({
            'success':True,
            'drinks': drinks
        }), 200

    except Exception as error:
        # raise appropriate status code reflecting the reason of failure
        raise error


# Done implement endpoint POST /drinks to create a new drink in the database
# Require Permission('post:drinks') that contain the drink.long() data representation for new drink
# Returns status code 200 and json {"success": True, "drinks": drink} where drink an array 
# containing only the newly created drink or appropriate status code indicating reason for failure   
 
@app.route('/drinks', methods=['POST'])
# use of requires_auth decorator to check permission 'post:drinks'
@requires_auth('post:drinks')
def create_drink(jwt):
    try:
        # get request body in json
        new_drink = request.get_json()
        # define title variable to get title from json object
        title = json.loads(request.data)['title']
        # check if title is empty abort with status code 400
        if title == '':
            abort(400)
        # prepare drink object to insert into drink table with attributes (title, recipe) 
        drink = Drink(
            title=new_drink.get('title'),
            recipe=json.dumps(new_drink.get('recipe'))
        )
        
        drink.insert()

        return jsonify({
            'success':True,
            'drinks': drink.long()
        }), 200

    except Exception as error:
        # raise appropriate status code reflecting the reason of failure
        raise error



# Done implement endpoint PATCH /drinks/<id> to update the corresponding row for <id>
# It will respond with a 404 error if <id> is not found
# Require the 'patch:drinks' permission that contain the drink.long() data representation for updated drink
# Returns status code 200 and json {"success": True, "drinks": drink} where drink
# an array containing only the updated drink or appropriate status code indicating reason for failure

@app.route('/drinks/<int:id>', methods=['PATCH'])
# use of requires_auth decorator to check permission 'patch:drinks'
@requires_auth('patch:drinks')
def update_drinks(jwt, id):
    try:
        # get drink from database for <id>
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        # get request body in json
        request_body = request.get_json()
        # check if no data in drink table for <id> abort with status code 404
        if not drink:
            abort(404)
        
        title = json.loads(request.data)['title']
        # check if title is empty abort with status code 400
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
        # raise appropriate status code reflecting the reason of failure
        raise error
    

# Done implement endpoint DELETE /drinks/<id> to delete the corresponding row for <id>
# It will respond with a 404 error if <id> is not found
# Require the 'delete:drinks' permission
# Returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record

@app.route('/drinks/<int:id>', methods=['DELETE'])
# use of requires_auth decorator to check permission 'delete:drinks'
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        # get drink from database for <id>
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        # check if no data in drink table for <id> abort with status code 404
        if not drink:
            abort(404)
        
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    except Exception as error:
        # raise appropriate status code reflecting the reason of failure
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
def bad_request(error):
    return jsonify({
    "success": False, 
    "error": 400,
    "message": "bad request"
    }), 400


# Done implement error handlers for resource not found
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
    "success": False, 
    "error": 404,
    "message": "resource not found"
    }), 404

# error handlers for method not allowed
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
    "success": False, 
    "error": 405,
    "message": "method not allowed"
    }), 405

# Done implement error handlers for server error
@app.errorhandler(500)
def server_error(error):
    return jsonify({
    "success": False, 
    "error": 500,
    "message": "Internal Server Error"
    }), 500

# Done implement error handlers for AuthError from class AuthError in auth.py
@app.errorhandler(AuthError)
def auth_error(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response
