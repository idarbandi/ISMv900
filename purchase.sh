#!/bin/bash

echo "===== Setting up Purchase Test Data ====="

# Activate the virtualenv
echo "Activating virtualenv 'venv'..."
source venv/bin/activate || { echo "Failed to activate virtualenv. Is it installed?"; exit 1; }
echo "Virtualenv activated successfully."

# Generate purchase-related test data
python manage.py shell -c "
# Import necessary modules
from myapp.models import Truck, Supplier, MaterialType, Unit, RawMaterial, ConsumptionProfile, Purchases
from django.utils import timezone
import random
from datetime import timedelta

# --- Create Truck ---
print('Creating truck for incoming delivery...')
truck = Truck(
    license_number='72ج538-21',
    driver_name='رضا احمدی',
    driver_doc='9876543210',
    phone='09361234567',
    status='Active',
    location='Entrance',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
truck.save()
print(f'Created Truck: {truck.license_number} - {truck.driver_name}')

# --- Create Supplier ---
print('Creating supplier...')
supplier = Supplier(
    supplier_name='صنایع کاغذ ستاره شرق',
    address='مشهد، شهرک صنعتی توس، فاز 2، خیابان دانش',
    phone='05135421789',
    status='Active',
    comments='تامین کننده اصلی کاغذ و مقوا',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
supplier.save()
print(f'Created Supplier: {supplier.supplier_name}')

# --- Create Material Type ---
print('Creating material type...')
material_type = MaterialType(
    supplier_name=supplier.supplier_name,
    material_type='کاغذ تست لاینر',
    status='Active',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
material_type.save()
print(f'Created Material Type: {material_type.supplier_name} - {material_type.material_type}')

# --- Create Unit ---
print('Creating unit...')
unit = Unit(
    supplier_name=supplier.supplier_name,
    material_type=material_type.material_type,
    unit_name='رول',
    count=10,
    status='Active',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
unit.save()
print(f'Created Unit: {unit.supplier_name} - {unit.material_type} - {unit.unit_name}')

# --- Create Raw Material ---
print('Creating raw material...')
raw_material = RawMaterial(
    supplier_name=supplier.supplier_name,
    material_type=material_type.material_type,
    material_name='تست لاینر 150 گرمی',
    status='Active',
    description='کاغذ تست لاینر با گراماژ 150 برای تولید لایه بیرونی کارتن',
    comments='کیفیت عالی با مقاومت بالا',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
raw_material.save()
print(f'Created Raw Material: {raw_material.supplier_name} - {raw_material.material_name}')

# --- Create Consumption Profile ---
print('Creating consumption profile...')
consumption_profile = ConsumptionProfile(
    profile_name='پروفایل تولید کارتن صادراتی',
    supplier_name=supplier.supplier_name,
    material_name=raw_material.material_name,
    material_type=material_type.material_type,
    unit=unit.unit_name,
    quantity=8,
    status='Active',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
consumption_profile.save()
print(f'Created Consumption Profile: {consumption_profile.profile_name} - {consumption_profile.material_name}')

print('\\nCreating purchase entry for incoming materials...')
purchase = Purchases(
    date=timezone.now(),
    receive_date=timezone.now(),
    material_type=material_type.material_type,
    material_name=raw_material.material_name,
    supplier_name=supplier.supplier_name,
    unit=unit.unit_name,
    quantity=10,
    quality='درجه یک',
    penalty=0,
    weight1=1250,
    weight2=250,
    net_weight=1000,
    price_per_kg=120000,
    vat=1800000,
    total_price=121800000,
    extra_cost=500000,
    invoice_status='پرداخت نشده',
    status='تحویل شده',
    payment_details='پرداخت 30 روزه',
    payment_date=timezone.now() + timedelta(days=30),
    invoice_number='INV-1401-385',
    document_info='فاکتور رسمی',
    comments='محموله خرید مواد اولیه برای تولید کارتن صادراتی',
    username='admin',
    logs='ایجاد شده توسط اسکریپت آزمایشی خرید'
)
purchase.save()
print(f'Created Purchase Entry for {purchase.material_name} from {purchase.supplier_name}')

print('\\nPurchase test data setup complete!')
print(f'\\nSummary of created objects:')
print(f'- Truck: {truck.license_number} ({truck.driver_name})')
print(f'- Supplier: {supplier.supplier_name}')
print(f'- Material Type: {material_type.material_type}')
print(f'- Unit: {unit.unit_name}')
print(f'- Raw Material: {raw_material.material_name}')
print(f'- Consumption Profile: {consumption_profile.profile_name}')
print(f'- Purchase Entry: {purchase.material_name} ({purchase.invoice_number})')
"

echo "===== Purchase Test Data Setup Completed =====" 