from marshmallow import Schema, fields, validate, ValidationError

class TenantSchema(Schema):
    id = fields.Int(dump_only=True)
    
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100, error="Name cannot be empty and must be less than 100 characters")
    )
    
    email = fields.Email(
        required=True,
        validate=[
            validate.Length(max=100, error="Email must be less than 100 characters"),
            validate.Email(error="Invalid email address")
        ]
    )
    
    property_id = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Property ID must be a positive integer")
    )

    # Optional: To serialize the related property data
    property = fields.Nested('PropertySchema', dump_only=True)
