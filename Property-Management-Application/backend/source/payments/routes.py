import logging
from source.auth.jwt import login_required
from source.payments.validation import PaymentSchema, UpdatePaymentSchema
from flask_restx import Resource, fields, Namespace
from flask import request
from .services import PaymentService
from marshmallow import ValidationError

payment_service = PaymentService()

# Define the namespace
payment_ns = Namespace('payments', description='Payment operations')

# Define the model for payment
payment_model = payment_ns.model('Payment', {
    'id': fields.Integer(description='The payment identifier'),
    'amount': fields.Float(required=True, description='The amount of the payment'),
    'date': fields.String(required=True, description='The date of the payment'),
    'description': fields.String(description='Description of the payment'),
})

@payment_ns.route('/')
class PaymentList(Resource):
    @payment_ns.doc(description='Add a new payment')
    @payment_ns.expect(payment_model, validate=True)
    @payment_ns.response(201, 'Payment successfully added', model=payment_model)
    @payment_ns.response(400, 'Invalid input')
    @payment_ns.response(500, 'Internal server error')
    @login_required
    def post(self):
        schema = PaymentSchema()
        try:
            data = schema.load(request.json)
            payment, status_code = payment_service.add_payment(data)
            return payment.to_dict(), status_code
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            logging.error(f"Unexpected error while adding payment: {str(e)}")
            return {'error': "An unexpected error occurred while adding the payment.", "details": str(e)}, 500

    @payment_ns.doc(description='Get all payments')
    @payment_ns.response(200, 'Payments found', model=payment_model, as_list=True)
    @payment_ns.response(500, 'Internal server error')
    @login_required
    def get(self):
        try:
            payments, status_code = payment_service.get_payments()
            return [payment.to_dict() for payment in payments], status_code
        except Exception as e:
            logging.error(f"Unexpected error while retrieving payments: {str(e)}")
            return {'error': "An unexpected error occurred while retrieving payments.", "details": str(e)}, 500

@payment_ns.route('/<int:id>')
class Payment(Resource):
    @payment_ns.doc(description='Get a payment by ID')
    @payment_ns.response(200, 'Payment found', model=payment_model)
    @payment_ns.response(404, 'Payment not found')
    @payment_ns.response(500, 'Internal server error')
    @login_required
    def get(self, id):
        try:
            payment, status_code = payment_service.get_payment(id)
            if payment:
                return payment.to_dict(), status_code
            return {'message': 'Payment not found'}, 404
        except Exception as e:
            logging.error(f"Unexpected error while retrieving payment by ID {id}: {str(e)}")
            return {'error': "An unexpected error occurred while retrieving the payment.", "details": str(e)}, 500

    @payment_ns.doc(description='Update a payment by ID')
    @payment_ns.expect(payment_model, validate=True)
    @payment_ns.response(200, 'Payment successfully updated', model=payment_model)
    @payment_ns.response(404, 'Payment not found')
    @payment_ns.response(400, 'Invalid input')
    @payment_ns.response(500, 'Internal server error')
    @login_required
    
    def post(self, id):
        schema = UpdatePaymentSchema()
        try:
            data = schema.load(request.json)
            payment, status_code = payment_service.update_payment(id, data)
            if payment:
                return payment.to_dict(), status_code
            return {'message': 'Payment not found'}, 404
        except ValidationError as e:
            custom_errors = {field: f"Invalid value for {field}: {', '.join(messages)}" 
                             for field, messages in e.messages.items()}
            return {'errors': custom_errors}, 400
        except Exception as e:
            logging.error(f"Unexpected error while updating payment with ID {id}: {str(e)}")
            return {'error': "An unexpected error occurred while updating the payment.", "details": str(e)}, 500

    @payment_ns.doc(description='Delete a payment by ID')
    @payment_ns.response(204, 'Payment successfully deleted')
    @payment_ns.response(404, 'Payment not found')
    @payment_ns.response(500, 'Internal server error')
    @login_required
    
    def delete(self, id):
        try:
            success, status_code = payment_service.delete_payment(id)
            if success:
                return {'message': 'Payment deleted successfully'}, status_code
            return {'message': 'Payment not found'}, 404
        except Exception as e:
            logging.error(f"Unexpected error while deleting payment with ID {id}: {str(e)}")
            return {'error': "An unexpected error occurred while deleting the payment.", "details": str(e)}, 500
