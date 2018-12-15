from flask import jsonify, request, abort
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256 as hasher
from ua_db import signUp, updateUser, changeActiveState, getPassHash, getAllUsers, getUser, checkMail, checkUsername
from ua_config import app


auth = HTTPBasicAuth()


@app.errorhandler(400)
def bad_request():
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden():
    return jsonify({'error': 'Forbidden!'}), 403

@app.errorhandler(404)
def not_found():
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error():
    return jsonify({'error' : 'Internal server error'}), 500


@app.route('/user/login', methods=['POST'])
# @auth.login_required
def login():
    if not request.json:
        return abort(400)

    uname_mail = request.json['uname_mail']

    is_mail = False
    if '@' in uname_mail:
        is_mail = True

    if hasher.verify(request.json['password'], getPassHash(uname_mail, is_mail)):
        return jsonify({'result': 'Success', 'id': uname_mail}), 200 # Password matches

    return jsonify({'result': 'Wrong password or email'}), 400 # Password does not match

@app.route('/user/register', methods=['POST'])
# @auth.login_required
def register():
    if not request.json:
        return abort(400)

    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    dob = request.json['dob']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if not checkMail(email):
        return jsonify({'result': 'Email is taken'}), 400

    if not checkUsername(username):
        return jsonify({'result': 'Username is taken'}), 400

    pass_hash = hasher.hash(password)
    new_user = signUp(name, surname, gender, dob, username, pass_hash, email)

    if not new_user:
        return abort(500)

    return jsonify({'result': 'Success', 'id': new_user.user_id}), 200

@app.route('/user/update', methods=['POST'])
@auth.login_required
def user_update():
    if not request.json:
        return abort(400)

    user_account_id = request.json['id']
    name = request.json['name']
    surname = request.json['surname']
    gender = request.json['gender']
    dob = request.json['dob']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if checkMail(email) is not None:
        return jsonify({'result': 'Email is taken'}), 400

    if checkUsername(username) is not None:
        return jsonify({'result': 'Username is taken'}), 400

    pass_hash = hasher.hash(password)
    updated_user = updateUser(user_account_id, name, surname, gender, dob, username, pass_hash, email)
    if not updated_user:
        return abort(500)

    return jsonify({'result': 'Success', 'id' : updated_user.user_id}), 200

# Get all users
@app.route('/user/get', methods=['GET'])
#@auth.login_required
def user_get_all():

    all_users = getAllUsers()
    users_json = []

    for user_obj in all_users:
        user_dict = user_obj.__dict__
        user_dict.pop('_sa_instance_state')
        users_json.append(user_dict)

    if users_json:
        return jsonify({'result': 'Success', 'users' : users_json}), 200
    return abort(500)

# Get spesific user
@app.route('/user/get/<int:user_id>', methods=['GET'])
# @auth.login_required
def user_get(user_id):
    user_obj = getUser(user_id)
    if user_obj is not None:
        return jsonify({'result': 'User cannot be found on database'}), 204

    user_dict = user_obj.__dict__
    user_dict.pop('_sa_instance_state')

    return jsonify({'result': 'Success', 'user': user_dict}), 200



@app.route('/user/de-activate', methods=['POST'])
@auth.login_required
def user_activate():
    is_admin = request.authorization
    if not is_admin:
        return abort(401)

    user_account_id = request.json['id']

    db_result = changeActiveState(user_account_id)
    if db_result is None:
        return abort(500)

    return jsonify({'result': 'Success', 'is_active' : db_result}), 200



# Validate the admin signin ##################TODO##########################
@auth.verify_password
def verify_password(username, password):
    # TODO: Change check if is admin in the database or not.
    if username == 'admin' and password == 'asdqwe123':
        return True
    return False



if __name__ == '__main__':
    app.run(debug=True, port=8000)
