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
from myapp.models import Customer, Shipments, Sales, Truck, Supplier, MaterialType, Unit, RawMaterial, ConsumptionProfile
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

# Initialize Faker
fake = Faker('fa_IR')  # Persian locale for Iranian names

# --- Create Trucks ---
truck_data = [
    {'license_number': '45ع978-33', 'driver_name': 'علی مرادی', 'driver_doc': '123456789', 'phone': '09123456789'},
    {'license_number': '68ط321-44', 'driver_name': 'محمد رضایی', 'driver_doc': '234567890', 'phone': '09234567890'},
    {'license_number': '24ی567-55', 'driver_name': 'حسین محمدی', 'driver_doc': '345678901', 'phone': '09345678901'},
]

created_trucks = []
for data in truck_data:
    truck = Truck(
        license_number=data['license_number'],
        driver_name=data['driver_name'],
        driver_doc=data['driver_doc'],
        phone=data['phone'],
        status='Free',
        location='Entrance',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    truck.save()
    created_trucks.append(truck)
    print(f\"Created Truck: {truck.license_number} - {truck.driver_name}\")

# --- Create Suppliers ---
supplier_data = [
    {'supplier_name': 'شرکت کاغذ سازی پارس', 'address': 'تهران، خیابان آزادی، پلاک 123', 'phone': '02112345678'},
    {'supplier_name': 'صنایع مقوای ایران', 'address': 'اصفهان، شهرک صنعتی، خیابان 5', 'phone': '03132345678'},
    {'supplier_name': 'کارتن سازی آذین', 'address': 'تبریز، جاده مخصوص کرج، کیلومتر 10', 'phone': '04142345678'},
]

created_suppliers = []
for data in supplier_data:
    supplier = Supplier(
        supplier_name=data['supplier_name'],
        address=data['address'],
        phone=data['phone'],
        status='Active',
        comments='تامین کننده مواد اولیه کاغذی',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    supplier.save()
    created_suppliers.append(supplier)
    print(f\"Created Supplier: {supplier.supplier_name}\")

# --- Create Customers ---
customer_data = [
    {'customer_name': 'چاپخانه گلستان', 'address': 'مشهد، خیابان امام رضا، پلاک 45', 'phone': '05132345678'},
    {'customer_name': 'بسته بندی نوین', 'address': 'شیراز، شهرک صنعتی، خیابان 8', 'phone': '07132345678'},
    {'customer_name': 'تولیدی کارتن البرز', 'address': 'کرج، جاده مخصوص، کیلومتر 5', 'phone': '02632345678'},
]

created_customers = []
for data in customer_data:
    customer = Customer(
        customer_name=data['customer_name'],
        address=data['address'],
        phone=data['phone'],
        status='Active',
        comments='مشتری دائمی',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    customer.save()
    created_customers.append(customer)
    print(f\"Created Customer: {customer.customer_name}\")

# --- Create Material Types ---
material_type_data = [
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ کرافت'},
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ تست لاینر'},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ فلوتینگ'},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ گلاسه'},
    {'supplier_name': created_suppliers[2].supplier_name, 'material_type': 'مقوای دوبلکس'},
]

created_material_types = []
for data in material_type_data:
    material_type = MaterialType(
        supplier_name=data['supplier_name'],
        material_type=data['material_type'],
        status='Active',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    material_type.save()
    created_material_types.append(material_type)
    print(f\"Created Material Type: {material_type.supplier_name} - {material_type.material_type}\")

# --- Create Units ---
unit_data = [
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ کرافت', 'unit_name': 'رول', 'count': 50},
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ تست لاینر', 'unit_name': 'بسته', 'count': 100},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ فلوتینگ', 'unit_name': 'کیلوگرم', 'count': 1000},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ گلاسه', 'unit_name': 'ورق', 'count': 5000},
    {'supplier_name': created_suppliers[2].supplier_name, 'material_type': 'مقوای دوبلکس', 'unit_name': 'میلی لیتر', 'count': 2000},
]

created_units = []
for data in unit_data:
    unit = Unit(
        supplier_name=data['supplier_name'],
        material_type=data['material_type'],
        unit_name=data['unit_name'],
        count=data['count'],
        status='Active',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    unit.save()
    created_units.append(unit)
    print(f\"Created Unit: {unit.supplier_name} - {unit.material_type} - {unit.unit_name}\")

# --- Create Raw Materials ---
raw_material_data = [
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ کرافت', 'material_name': 'کرافت 100 گرمی'},
    {'supplier_name': created_suppliers[0].supplier_name, 'material_type': 'کاغذ تست لاینر', 'material_name': 'تست لاینر 120 گرمی'},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ فلوتینگ', 'material_name': 'فلوتینگ 80 گرمی'},
    {'supplier_name': created_suppliers[1].supplier_name, 'material_type': 'کاغذ گلاسه', 'material_name': 'گلاسه 130 گرمی'},
    {'supplier_name': created_suppliers[2].supplier_name, 'material_type': 'مقوای دوبلکس', 'material_name': 'دوبلکس 350 گرمی'},
]

created_raw_materials = []
for data in raw_material_data:
    raw_material = RawMaterial(
        supplier_name=data['supplier_name'],
        material_type=data['material_type'],
        material_name=data['material_name'],
        status='Active',
        description='مواد اولیه با کیفیت برای تولید کاغذ و مقوا',
        comments='کیفیت خوب',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    raw_material.save()
    created_raw_materials.append(raw_material)
    print(f\"Created Raw Material: {raw_material.supplier_name} - {raw_material.material_name}\")

# --- Create Consumption Profiles ---
consumption_profile_data = [
    {
        'profile_name': 'پروفایل تولید کارتن',
        'supplier_name': created_suppliers[0].supplier_name,
        'material_name': 'کرافت 100 گرمی',
        'material_type': 'کاغذ کرافت',
        'unit': 'رول',
        'quantity': 10,
    },
    {
        'profile_name': 'پروفایل تولید کارتن',
        'supplier_name': created_suppliers[1].supplier_name,
        'material_name': 'فلوتینگ 80 گرمی',
        'material_type': 'کاغذ فلوتینگ',
        'unit': 'کیلوگرم',
        'quantity': 50,
    },
    {
        'profile_name': 'پروفایل تولید جعبه',
        'supplier_name': created_suppliers[1].supplier_name,
        'material_name': 'گلاسه 130 گرمی',
        'material_type': 'کاغذ گلاسه',
        'unit': 'ورق',
        'quantity': 100,
    },
    {
        'profile_name': 'پروفایل تولید جعبه',
        'supplier_name': created_suppliers[2].supplier_name,
        'material_name': 'دوبلکس 350 گرمی',
        'material_type': 'مقوای دوبلکس',
        'unit': 'میلی لیتر',
        'quantity': 75,
    },
]

created_consumption_profiles = []
for data in consumption_profile_data:
    consumption_profile = ConsumptionProfile(
        profile_name=data['profile_name'],
        supplier_name=data['supplier_name'],
        material_name=data['material_name'],
        material_type=data['material_type'],
        unit=data['unit'],
        quantity=data['quantity'],
        status='Active',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی',
    )
    consumption_profile.save()
    created_consumption_profiles.append(consumption_profile)
    print(f\"Created Consumption Profile: {consumption_profile.profile_name} - {consumption_profile.material_name}\")

# --- Create a Shipment ---
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
    license_number=created_trucks[0].license_number,
    customer_name=created_customers[0].customer_name,
    weight1=random.randint(500, 1000),
    unload_location='Main Warehouse',
    unit='کیلوگرم',
    quantity=random.randint(10, 100),
    quality='درجه یک',
    weight2=random.randint(200, 499),
    net_weight=str(random.randint(100, 400)),
    material_type='کاغذ کرافت',
    material_name='کرافت 100 گرمی',
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
    customer_name=created_customers[0],  # Using the customer we created
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
    profile_name=\"پروفایل تولید کارتن\",
    invoice_status='NA',  # Important: set to 'NA' as requested
    invoice_number=f\"INV-{random.randint(1000, 9999)}\",
    payment_details=\"تصفیه 30 روزه\",
    document_info=\"مستندات اصلی ارائه شده\",
    comments=\"سفارش آزمایشی برای تایید\",
    shipment=shipment,
    username='admin',
)
sale.save()
print(f\"Created Sale: ID {sale.id} with invoice_status='NA'\")

print(\"\nSummary of created objects:\")
print(f\"- Trucks: {len(created_trucks)}\")
print(f\"- Suppliers: {len(created_suppliers)}\")
print(f\"- Customers: {len(created_customers)}\")
print(f\"- Material Types: {len(created_material_types)}\")
print(f\"- Units: {len(created_units)}\")
print(f\"- Raw Materials: {len(created_raw_materials)}\")
print(f\"- Consumption Profiles: {len(created_consumption_profiles)}\")
print(f\"- Shipment: ID={shipment.id}, Material={shipment.material_name}\")
print(f\"- Sale: ID={sale.id}, Invoice Status={sale.invoice_status}\")
"

echo "===== Development Environment Setup Completed ====="
echo "Admin user created:"
echo "  Username: darbandi"
echo "  Email: darbandi@gmail.com"
echo "  Password: darbandidr99@gmail.com"

# Stop any running servers
echo "Stopping any running servers..."
pkill -f "python manage.py runserver" || true
pkill -f "node" || true

echo ""
echo "===== Starting Servers ====="

# Start the Django server in the background
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait for Django to start
echo "Waiting for Django server to start..."
sleep 5

# Navigate to frontend directory and start Vue server
if [ -d "frontend" ]; then
    echo "Starting Vue frontend server..."
    cd frontend && npm run serve &
    VUE_PID=$!
    cd ..
else
    echo "Frontend directory not found. Skipping Vue server startup."
fi

echo ""
echo "===== Development Environment Ready ====="
echo "Django server running at http://localhost:8000/"
echo "Vue frontend running at http://localhost:8080/"
echo ""
echo "Press Ctrl+C to stop all servers"

# Keep script running until user presses Ctrl+C
wait 