from .models import Payment
from source.payments.models import db
from sqlalchemy.exc import SQLAlchemyError

class PaymentService:

    def delete_payment_by_tenant(self, tenant_id):
        try:
            payments = Payment.query.filter_by(tenant_id=tenant_id).all()
            if not payments:
                return {"error": "No payments found for this tenant"}, 404

            for payment in payments:
                db.session.delete(payment)
            db.session.commit()
            return {"message": "Payments deleted successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def get_payment_by_tenant(self, tenant_id):
        try:
            payments = Payment.query.filter_by(tenant_id=tenant_id).all()
            if not payments:
                return {"error": "No payments found for this tenant"}, 404
            return payments, 200

        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def add_payment(self, data):
        try:
            new_payment = Payment(**data)
            db.session.add(new_payment)
            db.session.commit()
            return new_payment, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def get_payments(self):
        try:
            payments = Payment.query.all()
            return payments, 200

        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def get_payment(self, id):
        try:
            payment = Payment.query.get(id)
            if not payment:
                return {"error": "Payment not found"}, 404
            return payment, 200

        except SQLAlchemyError as e:
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def update_payment(self, id, data):
        try:
            payment = Payment.query.get(id)
            if not payment:
                return {"error": "Payment not found"}, 404

            for key, value in data.items():
                setattr(payment, key, value)
            db.session.commit()
            return payment, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    def delete_payment(self, id):
        try:
            payment, __ = self.get_payment(id)
            if not payment:
                return {"error": "Payment not found"}, 404

            db.session.delete(payment)
            db.session.commit()
            return payment, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error occurred", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500
