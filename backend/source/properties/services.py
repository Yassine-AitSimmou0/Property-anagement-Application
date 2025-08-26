from source.payments.services import PaymentService
from source.tenants.services import TenantService
from .models import Property
from source.properties.models import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

tenant_service = TenantService()

class PropertyService:
    
    def add_property(self, data):
        try:
            new_property = Property(
                name=data.get('name'),
                address=data.get('address'),
                type=data.get('type'),
                number_of_units=data.get('number_of_units'),
                rental_cost=data.get('rental_cost')
            )
            db.session.add(new_property)
            db.session.commit()
            return new_property, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred while adding the property.", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred while adding the property.", "details": str(e)}, 500

    def get_properties(self):
        try:
            properties = Property.query.all()

            return properties, 200

        except SQLAlchemyError as e:
            return {"error": "Database error occurred while retrieving properties.", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred while retrieving properties.", "details": str(e)}, 500

    def get_property(self, id):
        try:
            property = Property.query.get(id)
            if not property:
                return {"error": "Property not found"}, 404
            return property, 200

        except SQLAlchemyError as e:
            return {"error": "Database error occurred while retrieving the property.", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred while retrieving the property.", "details": str(e)}, 500

    def update_property(self, id, data):
        try:
            property = Property.query.get(id)
            if not property:
                return {"error": "Property not found"}, 404

            for key, value in data.items():
                setattr(property, key, value)
            db.session.commit()
            return property, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred while updating the property.", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred while updating the property.", "details": str(e)}, 500

    def delete_property(self, id):
        try:
            property = Property.query.get(id)
            if not property:
                return {"error": "Property not found"}, 404

            tenant_service.delete_tenant_by_property(id)
            db.session.delete(property)
            db.session.commit()
            return {"message": "Property deleted successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred while deleting the property.", "details": str(e)}, 500

        except Exception as e:
            db.session.rollback()
            return {"error": "An unexpected error occurred while deleting the property.", "details": str(e)}, 500
