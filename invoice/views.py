from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from myapp.models import Sales, Customer

import json
import traceback
from django.utils import timezone


@csrf_exempt
def test_api(request):
    """A simple test API endpoint to check if basic API functionality works"""
    try:
        return JsonResponse({
            'status': 'success',
            'message': 'Test API endpoint is working',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def latest_pending_sale(request):
    """Get the latest sale with invoice_status='NA'"""
    print("latest_pending_sale view called")
    
    try:
        # Check if any sales exist at all (for debugging)
        all_sales_count = Sales.objects.all().count()
        pending_sales_count = Sales.objects.filter(invoice_status='NA').count()
        print(f"Total sales: {all_sales_count}, Pending sales: {pending_sales_count}")
        
        # Get the latest sale with invoice_status='NA'
        sale = Sales.objects.filter(invoice_status='NA').order_by('-date').first()
        
        if not sale:
            print("No pending sales found")
            return JsonResponse({'message': 'No pending sales found'}, status=404)
        
        # Debug information
        print(f"Found sale: ID={sale.id}, invoice_status={sale.invoice_status}")
        
        # Try to get the customer info - handle both FK and CharField cases
        customer_data = None
        try:
            # If customer_name is a ForeignKey
            if hasattr(sale.customer_name, 'id'):
                customer = sale.customer_name
                customer_data = {
                    'id': customer.id,
                    'name': getattr(customer, 'customer_name', ''),
                    'economic_code': getattr(customer, 'economic_code', ''),
                    'postcode': getattr(customer, 'postcode', ''),
                    'phone': getattr(customer, 'phone', ''),
                    'national_id': getattr(customer, 'national_id', '')
                }
            # If customer_name is just a string
            else:
                customer_data = {
                    'id': None,
                    'name': str(sale.customer_name),
                    'economic_code': '',
                    'postcode': '',
                    'phone': '',
                    'national_id': ''
                }
        except Exception as e:
            print(f"Error getting customer data: {e}")
            customer_data = {
                'id': None,
                'name': str(getattr(sale, 'customer_name', 'Unknown')),
                'economic_code': '',
                'postcode': '',
                'phone': '',
                'national_id': ''
            }
        
        # Get the shipment info if it exists
        shipment_data = None
        try:
            if hasattr(sale, 'shipment') and sale.shipment:
                shipment = sale.shipment
                
                purchase_id = None
                if hasattr(shipment, 'purchase_id'):
                    if hasattr(shipment.purchase_id, 'id'):
                        purchase_id = shipment.purchase_id.id
                    else:
                        purchase_id = shipment.purchase_id
                
                shipment_data = {
                    'id': shipment.id,
                    'material_name': getattr(shipment, 'material_name', ''),
                    'purchase_id': purchase_id,
                    'quantity': getattr(shipment, 'quantity', 0),
                    'unit': getattr(shipment, 'unit', '')
                }
        except Exception as e:
            print(f"Error getting shipment data: {e}")
            # Continue without detailed shipment data
        
        # Prepare the sale data for the response
        data = {
            'id': sale.id,
            'date': sale.date.isoformat() if sale.date else None,
            'customer_name': str(getattr(sale, 'customer_name', 'Unknown')),
            'invoice_number': getattr(sale, 'invoice_number', ''),
            'invoice_status': sale.invoice_status,
            'price_per_kg': getattr(sale, 'price_per_kg', 0),
            'total_price': getattr(sale, 'total_price', 0),
            'customer': customer_data,
            'shipment': shipment_data
        }
        
        print("Successfully prepared response data")
        return JsonResponse(data)
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def simple_latest_pending_sale(request):
    """Get the latest sale with invoice_status='NA' - simplified version"""
    try:
        # Get the latest sale with invoice_status='NA'
        sale = Sales.objects.filter(invoice_status='NA').order_by('-date').first()
        
        if not sale:
            return JsonResponse({'message': 'No pending sales found'}, status=404)
        
        # Return minimal data
        data = {
            'id': sale.id,
            'date': str(sale.date) if sale.date else None,
            'invoice_status': sale.invoice_status,
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def invoice_page(request):
    return render(request, 'invoice.html')


@csrf_exempt
def sales_order_view(request, sale_id):
    sale = Sales.objects.get(id=sale_id)
    context = {
        'sale': sale,
        'can_confirm': sale.invoice_status == 'NA',
        'can_print': sale.invoice_status == 'sent',
    }
    return render(request, 'SalesOrder.html', context)


@csrf_exempt
def sales_order(request):
    """Render the sales order page which will fetch and show the latest pending invoice"""
    # Just render the template, the Vue component will handle the data loading
    return render(request, 'sales_order.html')


@csrf_exempt
def confirm_sales_invoice(request, sales_id=None):
    """Confirm a sales invoice by setting its status to 'Sent'"""
    print(f"confirm_sales_invoice called with sales_id: {sales_id}")
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is supported'}, status=405)
    
    try:
        # If sales_id is provided in the URL
        if sales_id:
            print(f"Looking for sale with ID: {sales_id}")
            sale = Sales.objects.get(id=sales_id)
        else:
            # Try to get sales_id from request body
            try:
                data = json.loads(request.body)
                sales_id = data.get('sales_id')
                print(f"Extracted sales_id from body: {sales_id}")
                if not sales_id:
                    return JsonResponse({'status': 'error', 'message': 'No sales_id provided'}, status=400)
                sale = Sales.objects.get(id=sales_id)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON in request body'}, status=400)
        
        print(f"Found sale: {sale}, current status: {sale.invoice_status}")
        
        # Only confirm if status is 'NA'
        if sale.invoice_status == 'NA':
            print("Updating status to 'Sent'")
            sale.invoice_status = 'Sent'
            sale.save()
            print("Sale saved successfully, status now:", sale.invoice_status)
            return JsonResponse({'status': 'success'})
        else:
            print(f"Cannot confirm: status is already {sale.invoice_status}")
            return JsonResponse({'status': 'error', 'message': f'Invoice already confirmed (status: {sale.invoice_status})'}, status=400)
    
    except Sales.DoesNotExist:
        print(f"Sales record not found for ID: {sales_id}")
        return JsonResponse({'status': 'error', 'message': 'Sales record not found'}, status=404)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def create_test_sale(request):
    """Create a test sale entry with invoice_status='NA'"""
    try:
        from myapp.models import Sales, Customer
        
        print("Attempting to create a test sale")
        
        # First check if we can create a test customer
        try:
            # Try to find an existing customer
            customer = Customer.objects.first()
            if not customer:
                # If no customer exists, create a test one
                customer = Customer(
                    customer_name="Test Customer",
                    date=timezone.now(),
                    status='Active'
                )
                customer.save()
                print(f"Created test customer with ID: {customer.id}")
        except Exception as customer_e:
            print(f"Error with customer: {customer_e}")
            customer = None
        
        # Create a simple Sale entry with minimal fields
        sale_kwargs = {
            'invoice_status': 'NA',
            'date': timezone.now(),
            'price_per_kg': 1000,
            'total_price': 50000
        }
        
        # Use customer as ForeignKey if available
        if customer:
            sale_kwargs['customer_name'] = customer
        else:
            sale_kwargs['customer_name'] = "Test Customer (String)"
        
        sale = Sales(**sale_kwargs)
        sale.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Test sale created with ID: {sale.id}',
            'sale_id': sale.id
        })
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)