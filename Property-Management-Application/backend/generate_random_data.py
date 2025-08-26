from source.payments.models import Payment
from source.properties.models import Property
from source.tenants.models import Tenant
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source.database import db  # Adjust this import according to your project structure

# Initialize Faker
fake = Faker()

# Create a new SQLAlchemy engine and session
DATABASE_URL = "postgresql+psycopg2://username:password@db:5432/property_management_db"  # Update with your database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def generate_random_properties(n=50):
    properties = []
    for _ in range(n):
        property_data = {
            'name': fake.word(),
            'address': fake.address(),
            'type': fake.word(),
            'number_of_units': fake.random_int(min=1, max=10),
            'rental_cost': fake.random_number(digits=4),
        }
        property_instance = Property(**property_data)
        properties.append(property_instance)
    return properties

def generate_random_tenants(n=50):
    tenants = []
    for _ in range(n):
        tenant_data = {
            'name': fake.name(),
            'email': fake.email(),
            'property_id': fake.random_int(min=1, max=50),
        }
        tenant_instance = Tenant(**tenant_data)
        tenants.append(tenant_instance)
    return tenants

def generate_random_payments(n=100):
    payments = []
    for _ in range(n):
        payment_data = {
            'date': fake.date_this_year(),
            'settled': fake.boolean(chance_of_getting_true=50),
            'amount': fake.random_number(digits=3),
            'tenant_id': fake.random_int(min=1, max=50),
        }
        payment_instance = Payment(**payment_data)
        payments.append(payment_instance)  
    return payments  


def main():
    # Generate and add properties
    properties = generate_random_properties()
    session.add_all(properties)
    session.commit()
    print("Inserted properties into the database.")

    # Generate and add tenants
    tenants = generate_random_tenants()
    session.add_all(tenants)
    session.commit()
    print("Inserted tenants into the database.")

    # Generate and add payments
    payments = generate_random_payments()
    session.add_all(payments)
    session.commit()
    print("Inserted payments into the database.")

if __name__ == "__main__":
    main()
