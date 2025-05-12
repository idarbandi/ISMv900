from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.conf import settings
from django.contrib.auth.decorators import login_required

from xhtml2pdf import pisa
from weasyprint import HTML

from myapp.models import Sales, Customer

import io
import json
import os
from datetime import datetime
import jdatetime
import tempfile
import base64
from django.utils import timezone


@csrf_exempt
def test_api(request):
    """A simple test API endpoint to check if basic API functionality works"""
    try:
        return JsonResponse({
            'status': 'success',
            'message': 'Test API endpoint is working',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
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
        print(f"Sale attributes: {dir(sale)}")
        print(f"Customer name type: {type(sale.customer_name)}")
        
        # Try to get the customer info - handle both FK and CharField cases
        customer_data = None
        try:
            # If customer_name is a ForeignKey
            if hasattr(sale.customer_name, 'id'):
                customer = sale.customer_name
                print(f"Customer is a related object: {customer}")
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
                print(f"Customer name is a string: {sale.customer_name}")
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
                print(f"Found shipment: {shipment}")
                
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
            else:
                print("No shipment found or not accessible")
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
        import traceback
        print("Exception in latest_pending_sale view:")
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
        import traceback
        print("Exception in simple_latest_pending_sale view:")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def invoice_page(request):
    return render(request, 'invoice.html')


@csrf_exempt
def havaleh(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Convert the current UTC time to Jalali
            current_time = datetime(2025, 5, 8, 13, 23, 21)  # Your provided timestamp
            jalali_datetime = jdatetime.datetime.fromgregorian(datetime=current_time)
            persian_date = jalali_datetime.strftime('%Y/%m/%d')  # Format as YYYY/MM/DD in Persian
            
            # Calculate total weight
            total_weight = 0
            for item in data.get('items', []):
                try:
                    total_weight += float(item.get('weight', 0))
                except (ValueError, TypeError):
                    pass

            context = {
                'date': persian_date,  # Use the Persian date here
                'serial': data.get('serial', ''),
                'items': data.get('items', []),
                'total_weight': f"{total_weight:,.0f}",
                'note': data.get('note', ''),
            }

            # Generate HTML
            html_string = render_to_string('havaleh.html', context)
            
            # Create PDF using WeasyPrint with base_url for static files
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
            pdf = html.write_pdf()
            
            # Return the PDF
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=havaleh_{data.get("serial", "")}.pdf'
            return response

        except Exception as e:
            print(f"Error: {str(e)}")  # For debugging
            return JsonResponse({
                'error': f'Server Error: {str(e)}',
                'status': 'error'
            }, status=500)

@csrf_exempt
def Purchases(request):
    if request.method == 'POST':

        items = []
        
        goods_codes = request.POST.getlist('goods_code')
        goods_comments_list = request.POST.getlist('goods_comments')
        goods_counts = request.POST.getlist('goods_count')
        units = request.POST.getlist('unit')
        unit_prices = request.POST.getlist('unit_price')

        total_price = 0
        total_taxes = 0

        for i in range(len(goods_codes)):
            try:
                count = int(goods_counts[i])
                price = float(unit_prices[i])
                subtotal = count * price
                tax = subtotal * 0.1
                total = subtotal + tax

                item = {
                    'goods_code': goods_codes[i],
                    'goods_comments': goods_comments_list[i],
                    'goods_count': count,
                    'unit': units[i],
                    'unit_price': price,
                    'subtotal': subtotal,
                    'tax': tax,
                    'total': total
                }

                items.append(item)
                total_price += subtotal
                total_taxes += tax
            except (ValueError, IndexError):
                continue  # Skip invalid input rows

        grand_total = total_price + total_taxes

        context = {
            'items': items,
            'total_price': total_price,
            'total_taxes': total_taxes,
            'grand_total': grand_total,
        }

    return render(request, 'Purchases.html')

@csrf_exempt
def generate_purchase_order_pdf(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            context = {
                'row': data.get('row', ''),
                'product_name': data.get('product_name', ''),
                'grammage': data.get('grammage', ''),
                'paper_width': data.get('paper_width', ''),
                'buyer_name': data.get('buyer_name', ''),
                'quantity': data.get('quantity', ''),
                'product_weight': data.get('product_weight', ''),
                'notes': data.get('notes', ''),
                'total': data.get('total', ''),
                'accounting': data.get('accounting', ''),
                'warehouse': data.get('warehouse', ''),
                'sales_manager': data.get('sales_manager', ''),
                'factory_manager': data.get('factory_manager', ''),
                'receiver': data.get('receiver', ''),
                'end_statement': data.get('end_statement', '')
            }

            html = render_to_string("purchaseorder.html", context)
            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=result)
            
            if pisa_status.err:
                return HttpResponse('خطا در تولید PDF', status=500)
                
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        except Exception as e:
            return HttpResponse(f"خطای داخلی: {str(e)}", status=500)
    else:
        return HttpResponse("فقط POST پشتیبانی می‌شود.", status=405)

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
        import traceback
        print("Error in confirm_sales_invoice:")
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def create_test_sale(request):
    """Create a test sale entry with invoice_status='NA'"""
    try:
        from myapp.models import Sales, Customer
        from django.utils import timezone
        
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
        
        # Check the Sales model fields
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(Sales)")
            columns = cursor.fetchall()
            print("Sales table columns:", columns)
        except Exception as e:
            print(f"Error getting table info: {e}")
        
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
        import traceback
        print("Error creating test sale:")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)