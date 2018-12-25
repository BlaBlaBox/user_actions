import requests
import pytest

# Usage pytest -q test.py

# link -> https://blablabox-auth.herokuapp.com


class TestClass(object):
    base_url = 'https://blablabox-auth.herokuapp.com'

    def test_get_all_user(self):
        r = requests.get(url=self.base_url+'/user/get')
        assert r.status_code == 200

    def test_register(self):
        l = {
            'email': 'test@test.com',
            'password': '123456',
            'name': 'test',
            'surname': 'test',
            'gender': 'O',
            'dob': '1994-12-19',
            'username': 'test'
        }

        r = requests.post(url=self.base_url + '/user/register', json=l)
        assert r.status_code == 200 or r.status_code == 400

    def test_login(self):
        l = {
            'uname_mail': 'test@test.com',
            'password': '123456'
        }

        r = requests.post(url=self.base_url + '/user/login', json=l)
        assert r.status_code == 200 or r.status_code == 400

    def test_user(self):

        r = requests.get(url=self.base_url + '/user/get/1')
        assert r.status_code == 200
