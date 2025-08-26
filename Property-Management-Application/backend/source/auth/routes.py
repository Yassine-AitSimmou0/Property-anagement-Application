# source/auth/routes.py
from source.auth.validation import LoginSchema, RegisterSchema
from flask import request
from source.auth.services import AuthService
from marshmallow import ValidationError
from flask_restx import Namespace, Resource, fields
from source.auth.jwt import login_required

# Initialize AuthService
auth_service = AuthService()

# Define the API namespace for authentication
auth_ns = Namespace('auth', description='Authentication operations')

# Define models for Swagger documentation
auth_model = auth_ns.model('Auth', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
})

login_model = auth_ns.model('Login', {
    'token': fields.String(description='JWT token'),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc(description='Register a new user')
    @auth_ns.expect(auth_model)
    @auth_ns.response(201, 'User successfully registered', model=auth_model)
    @auth_ns.response(400, 'Invalid input')
    def post(self):
        schema = RegisterSchema()
        try:
            data = schema.load(request.json)
            user, status_code = auth_service.register_user(data)
            if user:
                return user, status_code
            return {"message": "Registration failed"}, 400
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc(description='Login a user and return a JWT token')
    @auth_ns.expect(auth_model)
    @auth_ns.response(200, 'Login successful', model=login_model)
    @auth_ns.response(401, 'Invalid credentials')
    @auth_ns.response(400, 'Invalid input')

    def post(self):
        try:
            data = request.json
            print(data)
            token, status_code = auth_service.login_user(data)
            if token:
                return token, status_code
            return {"message": "Login failed"}, 401
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400