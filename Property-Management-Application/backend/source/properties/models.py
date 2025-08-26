from source.database import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    number_of_units = db.Column(db.Integer, nullable=True)
    rental_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "type": self.type,
            "number_of_units": self.number_of_units,
            "rental_cost": self.rental_cost,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
