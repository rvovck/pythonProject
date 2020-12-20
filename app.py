import data as data
from flask import Flask, request, abort, session, jsonify, render_template
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

engine = create_engine(DATABASE_CONNECTION)
Session = sessionmaker(bind=engine)
sessioner = Session()

app = Flask(__name__)
bcrypt = Bcrypt(app)


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
                user.password = password
                user.role = role
                sessioner.add(user)
                sessioner.commit()
                result = UserSchema().dump(user)
                return result

        except ValidationError as error:
            print(f'Error: {error.messages}')


@app.route('/ad', methods=['GET', 'POST'])
def create_ad():
    data = request.json
    if request.method == 'POST':
        try:
            ad_data = {'adId': data['adId'],
                       'title': data['title'],
                       'content': data['content'],
                       'author': data['author'],
                       'city': data['city']}

            ad = AdSchema().load(ad_data)
        except ValidationError:
            return abort(400, 'Bad Request')

        sessioner.add(ad)
        sessioner.commit()
        return 'Registered Successfully'
    if request.method == 'GET':
        ads = sessioner.query(Ad).all()
        result = AdSchema(many=True).dump(ads)
        results = {i: result[i] for i in range(0, len(result))}
        return results


@app.route('/ad/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_ad_by_adId(id):
    data = request.json
    if request.method == 'GET':
        ad = sessioner.query(Ad).filter(Ad.adId == id).one_or_none()
        if ad is None:
            abort(404, 'Not Found')
        result = AdSchema().dump(ad)
        return result
    if request.method == 'PUT':
        ad = sessioner.query(Ad).filter(Ad.adId == id).one_or_none()
        title = data['title']
        content = data['content']
        author = data['author']
        city = data['city']

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
        else:
            sessioner.delete(ad)
            sessioner.commit()
            return 'Deleted successfully'


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
