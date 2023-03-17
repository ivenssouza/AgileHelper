from ninja import Schema
#from pydantic import Field, EmailStr

from django.contrib.auth.models import User
from ninja import ModelSchema


class UserSchemaOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']

class UserSchemaIn(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserSchemaLogIn(Schema):
    username: str
    password: str