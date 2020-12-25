import data as data
import datetime
from flask import Flask, request, abort, session, jsonify, render_template, make_response
from wsgiref.simple_server import make_server
from models import *
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from schemas import UserSchema
from sqlalchemy import *
from markupsafe import escape
from sqlalchemy.orm import sessionmaker
from schemas import *
from sqlalchemy import *
from flask_jwt import jwt, jwt_required, current_identity
from functools import wraps


engine = create_engine('postgresql://postgres:976604745@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
sessioner = Session()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'secret'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = sessioner.query(User).filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/user', methods=['POST', 'PUT'])
def create_user():
    data = request.json
    if request.method == 'POST':
        try:
            user_data = {'userId': data['userId'],
                         'username': data['username'],
                         'password': bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                         'role': data['role']}

            user = UserSchema().load(user_data)
        except ValidationError as error:
            print(f'Error: {error.messages}')
            print(f'Error: {error.valid_data}')

        sessioner.add(user)
        sessioner.commit()
        return 'Successfully Registered'
    if request.method == 'PUT':
        try:
            user = sessioner.query(User).filter(User.userId == data['userId']).one_or_none()
            username = data['username']
            password = data['password']
            role = data['role']

            if user is None:
                abort(404, 'Not Found')
            else:
                user.username = username
                user.password = bcrypt.generate_password_hash(password).decode('utf-8')
                user.role = role
                sessioner.add(user)
                sessioner.commit()
                result = UserSchema().dump(user)
                return result

        except ValidationError as error:
            print(f'Error: {error.messages}')


@app.route('/login', methods=['POST'])
def login():
    password = request.json.get('password', None)
    username = request.json.get('username', None)
    user = sessioner.query(User).filter(User.username == username).one_or_none()

    if bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8'), 'username': username}), 200
    else:
        return abort(403, 'Invalid password')


@app.route('/ad', methods=['GET'])
def get_ad():
    ads = sessioner.query(Ad).all()
    result = AdSchema(many=True).dump(ads)
    results = {i: result[i] for i in range(0, len(result))}
    return results


@app.route('/ad', methods=['POST'])
@token_required
def create_ad(current_user):
    data = request.json
    try:
        ad_data = {'adId': data['adId'],
                   'title': data['title'],
                   'content': data['content'],
                   'author': current_user.username,
                   'city': data['city']}

        ad = AdSchema().load(ad_data)
    except ValidationError:
        return abort(400, 'Bad Request')

    sessioner.add(ad)
    sessioner.commit()
    return 'Registered Successfully'


@app.route('/ad/<id>', methods=['GET'])
def get_ad_by_id(id):
    ad = sessioner.query(Ad).filter(Ad.adId == id).one_or_none()
    if ad is None:
        abort(404, 'Not Found')
    result = AdSchema().dump(ad)
    return result


@app.route('/ad/<id>', methods=['PUT', 'DELETE'])
@token_required
def get_ad_by_adId(current_user, id):
    data = request.json

    if request.method == 'PUT':
        ad = sessioner.query(Ad).filter(Ad.adId == id).one_or_none()
        if current_user.username == ad.author:
            title = data['title']
            content = data['content']
            author = current_user.username
            city = data['city']
        if current_user.username != ad.author:
            return 'You can not change this ad'

        if ad is None:
            abort(404, 'Not Found')
        else:
            ad.title = title
            ad.content = content
            ad.author = author
            ad.city = city
            sessioner.add(ad)
            sessioner.commit()
            return 'Updated Successfully'

    if request.method == 'DELETE':
        ad = sessioner.query(Ad).filter(Ad.adId == id).one_or_none()
        if ad is None:
            abort(404, 'Not Found')
        elif current_user.username == ad.author:
            sessioner.delete(ad)
            sessioner.commit()
            return 'Deleted successfully'
        else:
            return 'You can not delete this ad'


@app.route('/ad/city/<city>', methods=['GET'])
def ad_city_get(city):
    cities = sessioner.query(Ad).filter(Ad.city == city).all()
    if cities is None:
        abort(404, 'Not Found')
    else:
        result = AdSchema(many=True).dump(cities)
        results = {i: result[i] for i in range(0, len(result))}
        return results


if __name__ == '__main__':
    app.run(debug=True)

