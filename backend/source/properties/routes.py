from source.auth.jwt import login_required
from source.properties.validation import PropertySchema
from flask_restx import Resource, fields, Namespace
from flask import request
from .models import Property
from source.properties.models import db
from .services import PropertyService
from marshmallow import ValidationError

property_service = PropertyService()

# Define the namespace
property_ns = Namespace('properties', description='Property operations')

# Define the model for property
property_model = property_ns.model('Property', {
    'id': fields.Integer(description='The property identifier'),
    'name': fields.String(required=True, description='The name of the property'),
    'address': fields.String(required=True, description='The address of the property'),
    'type': fields.String(required=True, description='The type of the property'),
    'number_of_units': fields.Integer(description='The number of units in the property'),
    'rental_cost': fields.Float(required=True, description='The rental cost of the property')
})

@property_ns.route('/')
class PropertyList(Resource):
    @property_ns.doc(description='Add a new property')
    @property_ns.expect(property_model, validate=True)
    @property_ns.response(201, 'Property successfully added', model=property_model)
    @property_ns.response(400, 'Invalid input')
    @login_required
    def post(self):
        schema = PropertySchema()
        try: 
            data = schema.load(request.json)
            property, status_code = property_service.add_property(data)
            return property.to_dict(), status_code
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred while adding the property.", "details": str(e)}, 500

    @property_ns.doc(description='Get all properties')
    @property_ns.response(200, 'Properties found', model=property_model, as_list=True)
    @property_ns.response(500, 'Internal server error')
    @login_required
    
    def get(self):
        try:
            properties, status_code = property_service.get_properties()
            return [property.to_dict() for property in properties], status_code
        except Exception as e:
            print(e)
            return {'error': "An unexpected error occurred while retrieving properties.", "details": str(e)}, 500

@property_ns.route('/<int:id>')
class Property(Resource):
    @property_ns.doc(description='Get a property by ID')
    @property_ns.response(200, 'Property found', model=property_model)
    @property_ns.response(404, 'Property not found')
    @property_ns.response(500, 'Internal server error')
    @login_required
    
    def get(self, id):
        try:
            property, status_code = property_service.get_property(id)
            if property:
                return property.to_dict(), status_code
            return {'message': 'Property not found'}, 404
        except Exception as e:
            return {'error': "An unexpected error occurred while retrieving the property.", "details": str(e)}, 500

    @property_ns.doc(description='Update a property by ID')
    @property_ns.expect(property_model, validate=True)
    @property_ns.response(200, 'Property successfully updated', model=property_model)
    @property_ns.response(404, 'Property not found')
    @property_ns.response(400, 'Invalid input')
    @property_ns.response(500, 'Internal server error')
    @login_required
    
    def post(self, id):
        schema = PropertySchema()
        try:
            data = schema.load(request.json)
            property, status_code = property_service.update_property(id, data)
            if property:
                return property.to_dict(), status_code
            return {'message': 'Property not found'}, 404
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred while updating the property.", "details": str(e)}, 500

    @property_ns.doc(description='Delete a property by ID')
    @property_ns.response(204, 'Property successfully deleted')
    @property_ns.response(404, 'Property not found')
    @property_ns.response(500, 'Internal server error')
    @login_required
    
    def delete(self, id):
        try:
            property, status_code = property_service.get_property(id)
            if property:
                property_service.delete_property(id)
                return {'message': 'Property deleted successfully'}, 204
            return {'message': 'Property not found'}, 404
        except Exception as e:
            return {'error': "An unexpected error occurred while deleting the property.", "details": str(e)}, 500
