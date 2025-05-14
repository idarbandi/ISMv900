#!/bin/bash

echo "===== Setting up Sales Test Data ====="

# Activate the virtualenv
echo "Activating virtualenv 'venv'..."
source venv/bin/activate || { echo "Failed to activate virtualenv. Is it installed?"; exit 1; }
echo "Virtualenv activated successfully."

# Generate sales-related test data
python manage.py shell -c "
# Import necessary modules
from myapp.models import Products, Customer, Truck, Anbar_Salon_Tolid, Shipments, Sales
from django.utils import timezone
import random
from datetime import timedelta
import time

# --- Create Customer ---
print('Creating customer for outgoing shipment...')
# Check if the customer already exists - using filter().first() to handle multiple results
customer = Customer.objects.filter(customer_name='شرکت صنایع بسته بندی تهران').first()
if customer:
    print(f'Using existing Customer: {customer.customer_name} (ID: {customer.id})')
else:
    # Create new customer if it doesn't exist
    customer = Customer(
        customer_name='شرکت صنایع بسته بندی تهران',
        address='تهران، شهرک صنعتی شمس آباد، بلوار گلستان، خیابان گل‌ها، پلاک 4',
        phone='02156785432',
        status='Active',
        economic_code='4113456789',
        postcode='1471456789',
        national_id='14005987652',
        comments='مشتری مهم برای کارتن‌های صادراتی',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی فروش'
    )
    customer.save()
    print(f'Created Customer: {customer.customer_name}')

# --- Create Truck for Outgoing Shipment ---
print('Creating truck for outgoing shipment...')
# Check if the truck already exists - using filter().first() to handle multiple results
truck = Truck.objects.filter(license_number='15ن793-61').first()
if truck:
    print(f'Using existing Truck: {truck.license_number} - {truck.driver_name} (ID: {truck.id})')
else:
    # Create new truck if it doesn't exist
    truck = Truck(
        license_number='15ن793-61',
        driver_name='محسن کریمی',
        driver_doc='7654321098',
        phone='09125678901',
        status='Active',
        location='Exit',
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی فروش'
    )
    truck.save()
    print(f'Created Truck: {truck.license_number} - {truck.driver_name}')

# --- Create 5 Different Reels (Products) ---
print('\\nCreating 5 different reel products...')
products = []

# Define product specs for variety
product_specs = [
    {
        'reel_number': '1001',
        'width': 100,
        'gsm': 150,
        'length': 2000,
        'grade': 'درجه یک',
        'breaks': 0,
        'comments': 'تست لاینر با کیفیت عالی برای صادرات',
    },
    {
        'reel_number': '1002',
        'width': 120,
        'gsm': 125,
        'length': 2500,
        'grade': 'درجه یک',
        'breaks': 0,
        'comments': 'فلوتینگ با پایه کرافت مناسب جعبه میوه',
    },
    {
        'reel_number': '1003',
        'width': 80,
        'gsm': 175,
        'length': 1800,
        'grade': 'درجه دو',
        'breaks': 1,
        'comments': 'کرافت لاینر برای جعبه‌های مقاوم',
    },
    {
        'reel_number': '1004',
        'width': 90,
        'gsm': 135,
        'length': 2200,
        'grade': 'درجه یک',
        'breaks': 0,
        'comments': 'بک‌لاینر برای داخل جعبه‌های کارتن',
    },
    {
        'reel_number': '1005',
        'width': 110,
        'gsm': 160,
        'length': 1900,
        'grade': 'درجه یک',
        'breaks': 1,
        'comments': 'میدل‌لاینر برای لایه میانی کارتن',
    }
]

# Generate a timestamp prefix for unique reel numbers
timestamp_prefix = str(int(time.time()))[-5:]  # Last 5 digits of current timestamp

for i, spec in enumerate(product_specs):
    # Add timestamp to make reel_number unique
    reel_number = timestamp_prefix + '-' + spec['reel_number']
    
    # Check if product with this reel_number already exists - using filter().first()
    product = Products.objects.filter(reel_number=reel_number).first()
    if product:
        print(f'Product with reel number {reel_number} already exists, skipping (ID: {product.id})')
        products.append(product)
        continue
    else:
        # Create the product record if it doesn't exist
        product = Products(
            location='Anbar_Salon_Tolid',
            status='In-stock',
            qr_code='QR-TEST-' + reel_number,
            reel_number=reel_number,
            width=spec['width'],
            gsm=spec['gsm'],
            length=spec['length'],
            breaks=spec['breaks'],
            grade=spec['grade'],
            profile_name='پروفایل تولید کارتن صادراتی',
            username='admin',
            comments=spec['comments'],
            receive_date=timezone.now() - timedelta(days=5-i),
            logs='ایجاد شده توسط اسکریپت آزمایشی فروش\\n'
        )
        product.save()
        products.append(product)
    
    # Create corresponding warehouse entry - using filter().first()
    anbar = Anbar_Salon_Tolid.objects.filter(reel_number=product.reel_number).first()
    if anbar:
        print(f'Warehouse entry for reel #{product.reel_number} already exists (ID: {anbar.id})')
    else:
        # Create if it doesn't exist
        anbar = Anbar_Salon_Tolid(
            date=timezone.now() - timedelta(days=5-i),
            reel_number=product.reel_number,
            status='In-stock',
            location='A' + str(i+1),
            username='admin',
            logs='ایجاد شده توسط اسکریپت آزمایشی فروش\\n'
        )
        anbar.save()
    
    print(f'Created Product {i+1}: Reel #{product.reel_number} - {product.gsm}gsm, {product.width}cm width')

# --- Create Shipment for the Products ---
print('\\nCreating outgoing shipment...')
# Add unique timestamp to logs
timestamp = str(int(time.time()))
shipment_log = f'ایجاد شده توسط اسکریپت آزمایشی فروش - زمان: {timestamp}'

shipment = Shipments(
    date=timezone.now(),
    license_number=truck.license_number,
    customer_name=customer.customer_name,
    weight1=5500,
    weight2=1500,
    net_weight=4000,
    username='admin',
    status='تحویل شده',
    shipment_type='Outgoing',
    payment_status='پرداخت شده',
    logs=shipment_log
)
shipment.save()
print(f'Created Shipment to {shipment.customer_name}')

# --- Create Sales Records for Products ---
print('\\nCreating sales records for the products...')
total_price = 0

# Check if there's already a Sales record with invoice_status='NA'
existing_na_sale = Sales.objects.filter(invoice_status='NA').first()
if existing_na_sale:
    print(f'Found existing Sale with invoice_status="NA" (ID: {existing_na_sale.id})')
    print('Setting invoice_status to "Sent" for new sales to avoid validation error')
    # We'll use 'Sent' for our new records
    sale_invoice_status = 'Sent'
else:
    # We can use 'NA' for only one record
    sale_invoice_status = 'NA'

for i, product in enumerate(products):
    # Update the product status and link to shipment
    product.status = 'Sold'
    product.shipment_id = shipment
    product.save()
    
    # Calculate a price based on product specs
    price = (product.gsm * 10000) + (product.width * 5000)
    
    # Set invoice_status to 'NA' for the first record only if no existing 'NA' records
    this_sale_invoice_status = sale_invoice_status
    if i == 0 and sale_invoice_status == 'NA':
        this_sale_invoice_status = 'NA'
    else:
        this_sale_invoice_status = 'Sent'
    
    # Create the sales record
    sale = Sales(
        date=timezone.now(),
        customer_name=customer,
        license_number=truck.license_number,
        list_of_reels=product.reel_number,
        width=product.width,
        price_per_kg=price / 10,  # Simple price calculation
        net_weight=3000,
        weight1=5000,
        weight2=2000,
        status='فروخته شده',
        shipment=shipment,
        invoice_status=this_sale_invoice_status,
        vat=price * 0.09,
        total_price=price,
        extra_cost=50000,
        username='admin',
        logs='ایجاد شده توسط اسکریپت آزمایشی فروش'
    )
    sale.save()
    total_price += price
    
    print(f'Created Sale for Reel #{product.reel_number} - Price: {price:,} ریال - Invoice Status: {this_sale_invoice_status}')

print('\\nSales test data setup complete!')
print(f'\\nSummary of created objects:')
print(f'- Customer: {customer.customer_name}')
print(f'- Truck: {truck.license_number} ({truck.driver_name})')
print(f'- Products: 5 different reels created')
print(f'- Shipment: ID {shipment.id} to {shipment.customer_name}')
print(f'- Total Sales Value: {total_price:,} ریال')
"

echo "===== Sales Test Data Setup Completed =====" 