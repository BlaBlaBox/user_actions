from flask import jsonify, request, abort
from passlib.hash import pbkdf2_sha256 as hasher
from ua_db import signUp, updateUser, getUserByMailOrUsername, getAllUsers, getUser, checkMail, checkUsername, jsonify_user_model
from ua_config import app


@app.errorhandler(400)
def bad_request(err):
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@app.errorhandler(401)
def unauthorized(err):
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden(err):
    return jsonify({'error': 'Forbidden!'}), 403

@app.errorhandler(404)
def not_found(err):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(err):
    return jsonify({'error' : 'Internal server error'}), 500

@app.errorhandler(503)
def service_unavailable(err):
    return jsonify({'error' : 'Service unavailable'}), 503




@app.route('/user/login', methods=['POST'])
def login():
    if not request.json:
        return abort(400)

    uname_mail = request.json['uname_mail']

    is_mail = False
    if '@' in uname_mail:
        is_mail = True

    user_obj = getUserByMailOrUsername(uname_mail, is_mail)

    if user_obj is None:
        return abort(503)

    if hasher.verify(request.json['password'], user_obj["pass_hash"]):
        return jsonify({'result': 'Success', 'user': user_obj}), 200 # Password matches

    return jsonify({'result': 'Wrong password or email'}), 400 # Password does not match


@app.route('/user/register', methods=['POST'])
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

    if checkMail(email):
        return jsonify({'result': 'Email is taken'}), 400

    if checkUsername(username):
        return jsonify({'result': 'Username is taken'}), 400

    pass_hash = hasher.hash(password)
    new_user = signUp(name, surname, gender, dob, username, pass_hash, email)

    if not new_user:
        return abort(503)

    return jsonify({'result': 'Success', 'id': new_user.user_id}), 200


@app.route('/user/update', methods=['POST'])
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

    if checkMail(email):
        return jsonify({'result': 'Email is taken'}), 400

    if checkUsername(username):
        return jsonify({'result': 'Username is taken'}), 400

    pass_hash = hasher.hash(password)
    updated_user = updateUser(user_account_id, name, surname, gender, dob, username, pass_hash, email)
    if not updated_user:
        return abort(500)

    return jsonify({'result': 'Success', 'id' : updated_user.user_id}), 200


# Get all users
@app.route('/user/get', methods=['GET'])
def user_get_all():

    all_users = getAllUsers()
    users_json = []

    for user_obj in all_users:
        users_json.append(jsonify_user_model(user_obj))

    if users_json:
        return jsonify(result='Success', users=users_json), 200
    return abort(503)


# Get spesific user
@app.route('/user/get/<int:user_id>', methods=['GET'])
def user_get(user_id):
    user = getUser(user_id)

    if user is None:
        return jsonify({'result': 'User cannot be found on database'}), 503

    return jsonify(result='Success', user=user), 200



if __name__ == '__main__':
    app.config.from_object('ua_config')
    app.run(debug=True, port=8000)
