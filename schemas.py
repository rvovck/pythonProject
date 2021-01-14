from marshmallow import Schema, fields, post_load, validate
from models import *

#from pythonProject.models import User, Ad

#required=True, error_messages={'required': 'Please enter username'}
class UserSchema(Schema):
    #userId = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Int(validate=validate.Range(min=1, max=2))

    @post_load()
    def make_user(self, data, **kwargs):
        return User(**data)


class AdSchema(Schema):
    #adId = fields.Int()
    title = fields.Str()
    content = fields.Str()
    author = fields.Str()
    city = fields.Str()

    @post_load
    def make_ad(self, data, **kwargs):
        return Ad(**data)

class CitySchema(Schema):
    #cityId = fields.Int()
    cityname = fields.Str()

    @post_load
    def make_city(self, data, **kwargs):
        return City(**data)