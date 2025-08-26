from flask import Flask, request
from source.config import Config
from source.auth.routes import auth_ns
from source.properties.routes import property_ns
from source.tenants.routes import tenant_ns
from source.payments.routes import payment_ns

from flask_restx import Api
from flask_cors import CORS
from flask_migrate import Migrate

# Import your models
from source.database import db


# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize the Flask-Migrate
migrate = Migrate(app, db)
# Initialize the Flask-RESTx API
api = Api(app, version='1.0', title='Property Management API',
          description='A simple API for managing properties, tenants, and payments')

# allow for cross-origin requests
CORS(app)

@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        return '', 204
    
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Add namespaces to API
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(property_ns, path='/api/properties')
api.add_namespace(tenant_ns, path='/api/tenants')
api.add_namespace(payment_ns, path='/api/payments')

if __name__ == '__main__':
    app.run(debug=True)
