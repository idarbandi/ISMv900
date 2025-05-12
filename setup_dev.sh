#!/bin/bash

# Display info message
echo "===== Starting Development Environment Setup ====="

# 1. Activate the virtualenv
echo "Activating virtualenv 'venv'..."
source venv/bin/activate || { echo "Failed to activate virtualenv. Is it installed?"; exit 1; }
echo "Virtualenv activated successfully."

# 2. Clear the database
echo "Clearing SQLite database..."
DB_FILE="local.sqlite3"
if [ -f "$DB_FILE" ]; then
    rm "$DB_FILE"
    echo "Database file $DB_FILE has been deleted."
else
    echo "Database file $DB_FILE not found. A new one will be created."
fi

# 3. Run migrations
echo "Running migrations..."
python manage.py migrate || { echo "Migration failed"; exit 1; }
echo "Migrations completed successfully."

# 4. Create superuser
echo "Creating superuser..."
# Use a non-interactive way to create superuser
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='darbandi').exists():
    User.objects.create_superuser('darbandi', 'darbandi@gmail.com', 'darbandidr99@gmail.com');
    print('Superuser created successfully');
else:
    print('Superuser already exists');
"

# 5. Run Python script to create test data
echo "Generating test data..."
python manage.py shell -c "
# Import necessary modules
from myapp.models import Customer, Shipments, Sales
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

# Initialize Faker
fake = Faker('fa_IR')  # Persian locale for Iranian names

# Create a Customer
customer = Customer(
    customer_name=fake.company(),
    date=timezone.now(),
    status='Active',
    address=fake.address(),
    phone=fake.phone_number(),
    economic_code=str(random.randint(1000000000, 9999999999)),
    postcode=str(random.randint(1000000000, 9999999999)),
    national_id=str(random.randint(10000000000, 99999999999)),
    username='admin',  # Assuming this is a required field
)
customer.save()
print(f\"Created Customer: {customer.customer_name} (ID: {customer.id})\")

# Create a Shipment
shipment = Shipments(
    date=timezone.now(),
    status='Delivered',
    location='Warehouse',
    receive_date=timezone.now() - timedelta(days=2),
    entry_time=timezone.now() - timedelta(days=2, hours=2),
    weight1_time=timezone.now() - timedelta(days=2, hours=1),
    weight2_time=timezone.now() - timedelta(days=1),
    exit_time=timezone.now() - timedelta(hours=12),
    shipment_type='Outgoing',
    license_number=f\"IR-{random.randint(10000, 99999)}\",
    customer_name=customer.customer_name,
    weight1=random.randint(500, 1000),
    unload_location='Main Warehouse',
    unit='Kg',
    quantity=random.randint(10, 100),
    quality='Premium',
    weight2=random.randint(200, 499),
    net_weight=str(random.randint(100, 400)),
    material_type='Paper',
    material_name='Premium White Paper',
    price_per_kg=random.randint(100000, 500000),
    total_price=random.randint(5000000, 50000000),
    vat=random.randint(500000, 5000000),
    username='admin',
)
shipment.save()
print(f\"Created Shipment: ID {shipment.id} ({shipment.material_name})\")

# Create a Sales instance with invoice_status 'NA'
sale = Sales(
    date=timezone.now(),
    status='Terms',
    customer_name=customer,  # Using the customer we created
    license_number=shipment.license_number,
    list_of_reels=\"R001, R002, R003\",
    width=random.randint(50, 200),
    weight1=shipment.weight1,
    weight2=shipment.weight2,
    net_weight=int(shipment.net_weight) if shipment.net_weight.isdigit() else 300,
    price_per_kg=shipment.price_per_kg,
    vat=shipment.vat,
    total_price=shipment.total_price,
    extra_cost=random.randint(100000, 1000000),
    profile_name=\"Standard Profile\",
    invoice_status='NA',  # Important: set to 'NA' as requested
    invoice_number=f\"INV-{random.randint(1000, 9999)}\",
    payment_details=\"Net 30\",
    document_info=\"Original documentation provided\",
    comments=\"Test sale for confirmation\",
    shipment=shipment,
    username='admin',
)
sale.save()
print(f\"Created Sale: ID {sale.id} with invoice_status='NA'\")

print(\"\nSummary of created objects:\")
print(f\"- Customer: ID={customer.id}, Name={customer.customer_name}\")
print(f\"- Shipment: ID={shipment.id}, Material={shipment.material_name}\")
print(f\"- Sale: ID={sale.id}, Invoice Status={sale.invoice_status}\")
print(\"\nTo test the confirmation functionality, use the API endpoint:\")
print(f\"/api/confirm-sales-invoice/{sale.id}/\")
"

echo "===== Development Environment Setup Completed ====="
echo "Admin user created:"
echo "  Username: darbandi"
echo "  Email: darbandi@gmail.com"
echo "  Password: darbandidr99@gmail.com"

# 6. Start the development server
echo ""
echo "Starting Django development server..."
python manage.py runserver 