from source.auth.jwt import login_required
from source.tenants.validation import TenantSchema
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from .models import Tenant
from source.tenants.models import db
from .services import TenantService
from marshmallow import ValidationError

# Define the namespace
tenant_ns = Namespace('tenants', description='Tenant operations')

tenant_service = TenantService()

# Define the model for tenant
tenant_model = tenant_ns.model('Tenant', {
    'id': fields.Integer(description='The tenant identifier'),
    'name': fields.String(required=True, description='The name of the tenant'),
    'email': fields.String(required=True, description='The email of the tenant'),
    'property_id': fields.Integer(required=True, description='The property identifier')
})


@tenant_ns.route('/')
class TenantList(Resource):
    @tenant_ns.doc(description='Add a new tenant')
    @tenant_ns.expect(tenant_model, validate=True)
    @tenant_ns.response(201, 'Tenant successfully added', model=tenant_model)
    @tenant_ns.response(400, 'Invalid input')
    @login_required
    def post(self):
        schema = TenantSchema()
        try:
            data = schema.load(request.json)
            tenant, status_code = tenant_service.add_tenant(data)
            return tenant.to_dict(), status_code
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred while adding the tenant.", "details": str(e)}, 500
    
    @tenant_ns.doc(description='Get all tenants')
    @tenant_ns.response(200, 'Tenants found', model=tenant_model, as_list=True)
    @tenant_ns.response(500, 'Internal server error')
    @login_required
    def get(self):
        try:
            tenants, status_code = tenant_service.get_tenants()
            return [tenant.to_dict() for tenant in tenants], status_code
        except Exception as e:
            return {'error': "An unexpected error occurred while retrieving tenants.", "details": str(e)}, 500

@tenant_ns.route('/<int:id>')
class Tenant(Resource):
    @tenant_ns.doc(description='Get a tenant by ID')
    @tenant_ns.response(200, 'Tenant found', model=tenant_model)
    @tenant_ns.response(404, 'Tenant not found')
    @tenant_ns.response(500, 'Internal server error')
    @login_required

    def get(self, id):
        try:
            tenant = tenant_service.get_tenant(id)
            if tenant:
                return tenant.to_dict(), 200
            return {'message': 'Tenant not found'}, 404
        except Exception as e:
            return {'error': "An unexpected error occurred while retrieving the tenant.", "details": str(e)}, 500

    @tenant_ns.doc(description='Update a tenant by ID')
    @tenant_ns.expect(tenant_model, validate=True)
    @tenant_ns.response(200, 'Tenant successfully updated', model=tenant_model)
    @tenant_ns.response(404, 'Tenant not found')
    @tenant_ns.response(400, 'Invalid input')
    @tenant_ns.response(500, 'Internal server error')
    @login_required

    def post(self, id):
        schema = TenantSchema()
        try:
            data = schema.load(request.json)
            tenant, status_code = tenant_service.update_tenant(id, data)
            if tenant:
                return tenant.to_dict(), status_code
            return {'message': 'Tenant not found'}, 404
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred while updating the tenant.", "details": str(e)}, 500

    @tenant_ns.doc(description='Delete a tenant by ID')
    @tenant_ns.response(204, 'Tenant successfully deleted')
    @tenant_ns.response(404, 'Tenant not found')
    @tenant_ns.response(500, 'Internal server error')
    @login_required

    def delete(self, id):
        try:
            tenant = tenant_service.get_tenant(id)
            if tenant:
                tenant_service.delete_tenant(id)
                return {'message': 'Tenant deleted successfully'}, 204
            return {'message': 'Tenant not found'}, 404
        except Exception as e:
            return {'error': "An unexpected error occurred while deleting the tenant.", "details": str(e)}, 500
