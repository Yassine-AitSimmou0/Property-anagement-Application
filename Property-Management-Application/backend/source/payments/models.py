from source.database import db

class Payment(db.Model):
    __tablename__ = 'payments'


    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    tenant = db.relationship('Tenant', backref=db.backref('payments', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    settled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "tenant": self.tenant.to_dict(),
            "amount": self.amount,
            "date": self.date.isoformat(),
            "settled": self.settled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }