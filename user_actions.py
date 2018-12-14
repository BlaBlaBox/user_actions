from flask import Flask, jsonify, request, abort
from passlib.hash import pbkdf2_sha256 as hasher
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from login import signUp
from datetime import date, datetime
from config import app

auth = HTTPBasicAuth()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 403


@app.route('/user/login', methods=['POST'])
@auth.login_required
def login():
    if not request.json:
        return jsonify({ 'error' : 'Your request is not JSON' }), 400
   
    print(request.json['email']) # TODO: You will use it for taking the password from db
    sqled_password = 'myPassword'
    hashed_password_from_db = hasher.hash(sqled_password) # TODO: Change this with sql
    user_id = 15 # TODO: Get ID

    # If password is same
    if pbkdf2_sha256.verify(request.json['password'], hashed_password_from_db):
        return jsonify({'result': 'Success', 'id': user_id}), 200 # Password matches
    else:
        return jsonify({'result': 'Wrong password or email'}), 400 # Password does not match

@app.route('/user/register', methods=['POST'])
# @auth.login_required
def register():
    if not request.json:
        return jsonify({ 'error' : 'Your request is not JSON' }), 400

    stri = hasher.hash("passw")
    datestr = "1997-01-01"

    signUp("ahmed", "kul", "M", datetime.strptime(datestr, "%Y-%m-%d"), "ahome2", stri, "ahmed2@deneme.com")

    return jsonify({'error' : 'calismiyor'}), 200

    # TODO: Send these to the db
    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    dob = request.json['dob']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # TODO: check email status
    email_result = True
    if not email_result:
        return jsonify({'result': 'Email is taken'}), 400 

    # TODO: check username status
    username_result = True
    if not username_result:
        return jsonify({'result': 'Username is taken'}), 400 

    # TODO: Create person object
    create_person_result, person_id = True, 15
    if not create_person_result:
        return jsonify({'result': 'Database is down'}), 500 

    # TODO: Check if correctly assigned to the db
    create_user_account_result, user_account_id = True, 15
    if not create_user_account_result: 
        return jsonify({'result': 'Database is down'}), 500 
    
    return jsonify({'result': 'Success', 'id': user_account_id}), 200 
    
@app.route('/user/update', methods=['POST'])
@auth.login_required
def user_update():
    if not request.json:
        return jsonify({ 'error' : 'Your request is not JSON' }), 400

    # TODO: Update db with these
    user_account_id = request.json['id']
    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    dob = request.json['dob']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # TODO: Update person object
    update_person_result, person_id = True, 15
    if not update_person_result:
        return jsonify({'result': 'Database is down'}), 500 

    # TODO: Update if correctly assigned to the db
    update_user_account_result, user_account_id = True, 15
    if not update_user_account_result: 
        return jsonify({'result': 'Database is down'}), 500 
    
    return jsonify({'result': 'Success'}), 200 
   
# Get all users
@app.route('/user/get', methods=['GET'])
@auth.login_required
@auth.login_required
def user_get_all():
    # TODO: Take all trasactions from the db
    all_users = []

    # TODO: Result of the database get action
    result = True 
    
    if result:
        return jsonify({'result': 'Success'}), 200 # TODO: Send all users in JSON format
    else:
        return jsonify({'result': 'Database is down'}), 500 

# Get spesific user
@app.route('/user/get/<int:user_id>', methods=['GET'])
@auth.login_required
@auth.login_required
def user_get(user_id):
    # TODO: Result of the database get action
    result = True 

    if result:
        return jsonify({'result': 'Success', 'user': user_id}), 200 # TODO: Send send spesific user.
    else:
        return jsonify({'result': 'Database is down'}), 500 

@app.route('/user/deactivate', methods=['POST'])
@auth.login_required
def user_deactivate():
    # is_admin = ??
    # if not is_admin:
    #     return jsonify({'result': 'You are not an admin'}), 401 

    user_account_id = request.json['id'] # TODO: Use it for db

    # TODO: Change user is_active
    db_result = True
    if not db_result: 
        return jsonify({'result': 'Database is down'}), 500 

    return jsonify({'result': 'Success'}), 200 


@app.route('/user/activate', methods=['POST'])
@auth.login_required
def user_activate():
    is_admin = request.authorization
    if not is_admin:
        return jsonify({'result': 'You are not an admin'}), 401 

    user_account_id = request.json['id'] # TODO: Use it for db

    # TODO: Change user is_active
    db_result = True
    if not db_result: 
        return jsonify({'result': 'Database is down'}), 500 

    return jsonify({'result': 'Success'}), 200 

# Validate the admin signin
@auth.verify_password
def verify_password(username, password):
    # TODO: Change check if is admin in the database or not.
    if username == 'admin' and password == 'asdqwe123':
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True, port=8000) 