from marshmallow import Schema, fields, validate, ValidationError

class PropertySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, error="Name cannot be empty")
    )
    address = fields.Str(
        required=True, 
        validate=validate.Length(min=1, error="Address cannot be empty")
    )
    type = fields.Str(
        required=True, 
        validate=validate.Length(min=1, error="Type cannot be empty")
    )
    number_of_units = fields.Int(
        validate=validate.Range(min=0, error="Number of units cannot be negative")
    )
    rental_cost = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, error="Rental cost must be greater than 0")
    )
