from ninja import Schema
from uuid import UUID
from django.contrib.auth.models import User
from ninja import ModelSchema


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = "__all__"

class UserSchemaOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']

class UserSchemaIn(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ParticipantSchema(Schema):
    id: UUID
    user: UserSchemaOut

class ParticipantSchemaIn(Schema):
    user: UserSchemaIn
