import pytest
import requests
import json
from flask_jwt_extended import create_access_token, JWTManager
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = '12345678'
jwt = JWTManager(app)


def test_valid_login():
    url = 'http://127.0.0.1:5000/user/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'user11',
            'password': '1'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 200

def test_invalid_login():
    url = 'http://127.0.0.1:5000/user/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'us',
            'password': '999'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 404


def test_missing_password_login():
    url = 'http://127.0.0.1:5000/user/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'John'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_missing_username():
    url = 'http://127.0.0.1:5000/user/login'
    headers = {"Content-Type": "application/json"}

    data = {'password': '12345'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_invalid_password():
    url = 'http://127.0.0.1:5000/user/login'
    headers = {"Content-Type": "application/json"}

    data = {'username': 'user11',
            'password': '98765'}

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data)
    assert response.status_code == 403


