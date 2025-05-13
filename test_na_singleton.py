#!/usr/bin/env python
"""
This script tests the singleton constraint for Sales records with invoice_status='NA'.
It first creates one Sales record with invoice_status='NA', then attempts to create a second one,
which should fail due to the validation in the Sales model.

Run this script with: python manage.py shell < test_na_singleton.py
"""

from django.utils import timezone
from django.core.exceptions import ValidationError
from myapp.models import Sales, Customer, Shipments
import sys

# Helper function to print to stderr in color
def print_color(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'end': '\033[0m'
    }
    print(f"{colors[color]}{text}{colors['end']}", file=sys.stderr)

print_color("\n=== Testing Sales NA Invoice Status Singleton Constraint ===", "blue")

try:
    # Get a customer for our test sales
    customer = Customer.objects.first()
    if not customer:
        print_color("Creating a test customer...", "yellow")
        customer = Customer.objects.create(
            customer_name="Test Customer",
            address="Test Address",
            phone="123456789",
            username="admin"
        )
    
    # Get a shipment for our test sales
    shipment = Shipments.objects.filter(shipment_type='Outgoing').first()
    if not shipment:
        print_color("No Outgoing shipment found. Creating a test shipment...", "yellow")
        shipment = Shipments.objects.create(
            license_number="TEST-123",
            customer_name="Test Customer",
            shipment_type="Outgoing",
            status="Delivered",
            location="Delivered",
            username="admin"
        )
    
    # Check if there are any existing NA sales
    existing_na_sales = Sales.objects.filter(invoice_status='NA')
    if existing_na_sales.exists():
        print_color(f"Existing NA sales found with ID: {existing_na_sales.first().id}", "yellow")
        print_color("Deleting existing NA sales for clean test...", "yellow")
        existing_na_sales.delete()
    
    # Create first sales record with invoice_status='NA'
    print_color("\nStep 1: Creating first Sales record with invoice_status='NA'", "blue")
    first_sale = Sales(
        date=timezone.now(),
        status='Terms',
        customer_name=customer,
        license_number="TEST-123",
        list_of_reels="TEST1,TEST2",
        width=100,
        weight1=1000,
        weight2=500,
        net_weight=500,
        price_per_kg=10000,
        vat=9,
        total_price=5000000,
        extra_cost=100000,
        profile_name="Test Profile",
        invoice_status='NA',  # This is the key field we're testing
        invoice_number="INV-001",
        payment_details="Test Payment",
        document_info="Test Document",
        comments="First test sale with NA status",
        shipment=shipment,
        username="admin"
    )
    
    try:
        first_sale.save()
        print_color(f"✅ Successfully created first Sales record with ID: {first_sale.id} and invoice_status='NA'", "green")
    except ValidationError as e:
        print_color(f"❌ Failed to create first Sales record: {e}", "red")
        sys.exit(1)
    
    # Try to create a second sales record with invoice_status='NA'
    print_color("\nStep 2: Attempting to create second Sales record with invoice_status='NA'", "blue")
    second_sale = Sales(
        date=timezone.now(),
        status='Terms',
        customer_name=customer,
        license_number="TEST-456",
        list_of_reels="TEST3,TEST4",
        width=100,
        weight1=1000,
        weight2=500,
        net_weight=500,
        price_per_kg=10000,
        vat=9,
        total_price=5000000,
        extra_cost=100000,
        profile_name="Test Profile",
        invoice_status='NA',  # This should cause validation error
        invoice_number="INV-002",
        payment_details="Test Payment",
        document_info="Test Document",
        comments="Second test sale with NA status - should fail",
        shipment=shipment,
        username="admin"
    )
    
    try:
        second_sale.save()
        print_color("❌ ERROR: Second Sales record was created! The singleton constraint is not working.", "red")
    except ValidationError as e:
        print_color(f"✅ Successfully prevented creation of second 'NA' sales record.", "green")
        print_color(f"✅ Validation error: {e}", "green")
    
    # Clean up - optional
    print_color("\nCleaning up test data...", "blue")
    first_sale.delete()
    print_color("Test data deleted.", "green")
    
    print_color("\n=== Test Complete ===", "blue")

except Exception as e:
    print_color(f"\n❌ Unexpected error during test: {e}", "red")
    import traceback
    traceback.print_exc() 