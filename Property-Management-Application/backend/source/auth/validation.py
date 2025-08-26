from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=4, max=25))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=35))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=35))