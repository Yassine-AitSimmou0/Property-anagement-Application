from werkzeug.security import generate_password_hash, check_password_hash
from source.auth.jwt import generate_token
from datetime import datetime, timedelta
from source.auth.models import User, db
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
import pytz


class AuthService:

    def register_user(self, data):
        try:
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                return {"error": "User already exists"}, 409

            # Hash the user's password
            hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

            # Create a new user
            new_user = User(
                name=data['name'],
                email=data['email'],
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            return {"id": new_user.id, "name": new_user.name, "email": new_user.email}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def login_user(self, data):
        try:
            # Fetch user by email
            user = User.query.filter_by(email=data['email']).first()
            print(user)
            if not user or not check_password_hash(user.password, data['password']):
                return {"error": "Invalid email or password"}, 401

            
            # Generate JWT token
            token = generate_token(user.id) 

            return {"token": token}, 200

        except ExpiredSignatureError:
            return {"error": "Token has expired"}, 401

        except InvalidTokenError:
            return {"error": "Invalid token"}, 401

        except DecodeError:
            return {"error": "Token decode failed"}, 401

        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500
