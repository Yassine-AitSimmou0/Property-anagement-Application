from datetime import date
from source.payments.services import PaymentService
from sqlalchemy.exc import IntegrityError
from .models import Tenant
from source.tenants.models import db
from marshmallow import ValidationError

payment_service = PaymentService()

class TenantService:

    def delete_tenant_by_property(self, property_id):
        try:
            tenants = Tenant.query.filter_by(property_id=property_id).all()
            if not tenants:
                return {"error": "No tenants found for this property"}, 404
            
            for tenant in tenants:
                payment_service.delete_payment_by_tenant(tenant.id)
                db.session.delete(tenant)
            db.session.commit()
            return {"message": "Tenants deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": "An error occurred while deleting the tenants.", "details": str(e)}, 500

    def get_tenant_by_property(self, property_id):
        try:
            tenants = Tenant.query.filter_by(property_id=property_id).all()
            if not tenants:
                return {"error": "No tenants found for this property"}, 404
            return tenants, 200

        except Exception as e:
            return {"error": "An error occurred while retrieving tenants.", "details": str(e)}, 500

    def add_tenant(self, data):
        try:
            new_tenant = Tenant(**data)
            db.session.add(new_tenant)
            db.session.commit()

            # Add a payment starting from the next month select date dynamically
            payment_data = {
                "tenant_id": new_tenant.id,
                "amount": new_tenant.property.rental_cost,
                "date": date.today().replace(day=1),
            }
            
            payment_service.add_payment(payment_data)
            return new_tenant, 201

        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key value" in str(e):
                return {"error": "This email is already in use."}, 409
            return {"error": "Database integrity error occurred.", "details": str(e)}, 500

        except ValidationError as e:
            return {"error": "Validation error occurred.", "details": str(e)}, 400

        except Exception as e:
            return {"error": "An unexpected error occurred.", "details": str(e)}, 500

    def get_tenants(self):
        try:
            tenants = Tenant.query.all()
            return tenants, 200

        except Exception as e:
            return {"error": "An error occurred while retrieving tenants.", "details": str(e)}, 500

    def get_tenant(self, id):
        try:
            tenant = Tenant.query.get(id)
            if not tenant:
                return {"error": "Tenant not found"}, 404
            return tenant, 200

        except Exception as e:
            return {"error": "An error occurred while retrieving the tenant.", "details": str(e)}, 500

    def update_tenant(self, id, data):
        try:
            tenant = Tenant.query.get(id)
            if not tenant:
                return {"error": "Tenant not found"}, 404

            for key, value in data.items():
                setattr(tenant, key, value)
            db.session.commit()
            return tenant, 200

        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key value" in str(e):
                return {"error": "This email is already in use."}, 409
            return {"error": "Database integrity error occurred.", "details": str(e)}, 500

        except ValidationError as e:
            return {"error": "Validation error occurred.", "details": str(e)}, 400

        except Exception as e:
            return {"error": "An unexpected error occurred.", "details": str(e)}, 500

    def delete_tenant(self, id):
        try:
            tenant = Tenant.query.get(id)
            if not tenant:
                return {"error": "Tenant not found"}, 404
            
            payment_service.delete_payment_by_tenant(id)
            db.session.delete(tenant)
            db.session.commit()
            return {"message": "Tenant deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": "An error occurred while deleting the tenant.", "details": str(e)}, 500
