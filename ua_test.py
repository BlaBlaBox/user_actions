import requests
import random
import string


# Usage: pytest ua_test.py


class UserAction():
    # base_url = 'https://blablabox-auth.herokuapp.com'

    # For local testing
    base_url = 'http://127.0.0.1:8000'

    # The test function for getting all users
    def get_all_user(self, required_status):
        r = requests.get(url=self.base_url + '/user/get')
        assert r.status_code == required_status

    # The test function for registering the user
    def register(self, user_info, required_status):
        r = requests.post(url=self.base_url + '/user/register', json=user_info)
        assert r.status_code == required_status

    # The test function for login
    def login(self, user_info, required_status):
        r = requests.post(url=self.base_url + '/user/login', json=user_info)
        assert r.status_code == required_status

    # The test function for geting one user
    def get_user(self, user_id, required_status):
        r = requests.get(url=self.base_url + '/user/get/' + user_id)
        assert r.status_code == required_status

    def send_end_test(self, status):
        resp = requests.get(self.base_url + "/endtest")
        assert resp.status_code == status


def test_user_actions():
    uAction = UserAction()

    # Valid User
    user_login_info = {
        'uname_mail': 'test@test.com',
        'password': '123456'
    }

    # Taken username and email
    user_register_info = {
        'email': 'test@test.com',
        'password': '123456',
        'name': 'test',
        'surname': 'test',
        'gender': 'O',
        'dob': '1994-12-19',
        'username': 'test'
    }

    # Get all user first
    uAction.get_all_user(200)

    # Try to login with valid email and password
    uAction.login(user_login_info, 200)

    # Try to login with user that does not exist
    user_login_info_temp = user_login_info.copy()
    user_login_info_temp['uname_mail'] = 'test@testest.com'
    uAction.login(user_login_info_temp, 503)

    # Try to login with invalid password
    user_login_info_temp = user_login_info.copy()
    user_login_info_temp['password'] += '7'
    uAction.login(user_login_info_temp, 400)

    # Try to login by sending integer password instead of string
    user_login_info_temp = user_login_info.copy()
    user_login_info_temp['password'] = 12345
    uAction.login(user_login_info_temp, 500)

    # Try to register with info that got already taken
    uAction.register(user_register_info, 400)

    # Try to register with misleading information about gender
    user_register_info_temp = user_register_info.copy()
    user_register_info_temp['email'] = create_random_string(4) + '@' + create_random_string(4) + '.com'
    user_register_info_temp['username'] = create_random_string(6)
    user_register_info_temp['gender'] = 'Other'  # This should be 'O' instead of 'Other'
    uAction.register(user_register_info_temp, 500)

    # Try to register with info that is not taken
    user_register_info_temp = user_register_info.copy()
    user_register_info_temp['email'] = create_random_string(4) + '@' + create_random_string(4) + '.com'
    user_register_info_temp['username'] = create_random_string(6)
    uAction.register(user_register_info_temp, 200)

    # Try to login with the user we have just registered
    user_login_info_temp = user_login_info.copy()
    user_login_info_temp['uname_mail'] = user_register_info_temp['email']
    user_login_info_temp['password'] = user_register_info_temp['password']
    uAction.login(user_login_info_temp, 200)

    # Try to get admin user
    uAction.get_user(str(1), 200)

    # Try to get the user that we do not have
    uAction.get_user(str(10000000000), 503)

    # Send a request to complete coverage report
    uAction.send_end_test(200)


def create_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
