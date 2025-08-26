from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)  # This field is for output only
    tenant_id = fields.Int(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S')
    settled = fields.Bool(missing=False)
    created_at = fields.DateTime(dump_only=True, format='%Y-%m-%dT%H:%M:%S')
    updated_at = fields.DateTime(dump_only=True, format='%Y-%m-%dT%H:%M:%S')

class UpdatePaymentSchema(Schema):
    amount = fields.Float(validate=validate.Range(min=0), optional=True)
    date = fields.DateTime(format='%Y-%m-%dT%H:%M:%S', optional=True)
    settled = fields.Bool()
