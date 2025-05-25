from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import io
import json
from django.http import HttpResponse, JsonResponse
from weasyprint import HTML
import tempfile
from datetime import datetime
import jdatetime
import base64
from django.contrib.staticfiles import finders
import os
from django.conf import settings

# New
from django.contrib.auth.decorators import login_required
from io import BytesIO
from myapp.models import Sales, Customer
import traceback
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize


@csrf_exempt
def invoice_page(request):
    return render(request, 'invoice.html')


# @csrf_exempt
# def havaleh(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
            
#             # Convert the current UTC time to Jalali
#             current_time = datetime(2025, 5, 8, 13, 23, 21)  # Your provided timestamp
#             jalali_datetime = jdatetime.datetime.fromgregorian(datetime=current_time)
#             persian_date = jalali_datetime.strftime('%Y/%m/%d')  # Format as YYYY/MM/DD in Persian
            
#             # Calculate total weight
#             total_weight = 0
#             for item in data.get('items', []):
#                 try:
#                     total_weight += float(item.get('weight', 0))
#                 except (ValueError, TypeError):
#                     pass

#             context = {
#                 'date': persian_date,  # Use the Persian date here
#                 'serial': data.get('serial', ''),
#                 'items': data.get('items', []),
#                 'total_weight': f"{total_weight:,.0f}",
#                 'note': data.get('note', ''),
#             }

#             # Generate HTML
#             html_string = render_to_string('havaleh.html', context)
            
#             # Create PDF using WeasyPrint with base_url for static files
#             html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
#             pdf = html.write_pdf()
            
#             # Return the PDF
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename=havaleh_{data.get("serial", "")}.pdf'
#             return response

#         except Exception as e:
#             print(f"Error: {str(e)}")  # For debugging
#             return JsonResponse({
#                 'error': f'Server Error: {str(e)}',
#                 'status': 'error'
#             }, status=500)


@csrf_exempt
def havaleh(request):
    """Generate a PDF for the havaleh (delivery form)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)
    
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Get all the form data
        date = data.get('date', '')
        serial = data.get('serial', '')
        items = data.get('items', [])
        note = data.get('note', '')
        invoice_id = data.get('invoice_id')
        
        # Process date using PersianDateText if available
        persian_date = date
        try:
            # Import here to avoid circular imports
            from invoice.utils import PersianDateText
            
            # Parse date if it's in format like "1403/03/15"
            if date and '/' in date:
                date_parts = date.split('/')
                if len(date_parts) == 3:
                    persian_date_obj = PersianDateText(date_parts)
                    persian_date = persian_date_obj.to_text()
        except Exception as e:
            print(f"Error processing Persian date: {e}")
            # Continue with original date
        
        # Calculate total weight and convert weights to Persian text
        total_weight = 0
        processed_items = []
        
        for item in items:
            weight = float(item.get('weight', 0))
            total_weight += weight
            
            # Create a copy of the item with Persian weight
            item_copy = item.copy()
            
            # Format weight with commas
            weight_persian = f"{weight:,.0f}"
            item_copy['weight_persian'] = weight_persian
            
            processed_items.append(item_copy)
        
        # Format total weight with Persian numerals
        total_weight_persian = f"{total_weight:,.0f}"
        
        # Prepare context for template
        context = {
            'date': date,
            'persian_date': persian_date,
            'serial': serial,
            'items': processed_items,
            'note': note,
            'total_weight': f"{total_weight:,.0f}",
            'total_weight_persian': total_weight_persian
        }
        
        # If invoice_id is provided, update the related Invoice record
        if invoice_id:
            try:
                # Import Invoice model here to avoid circular imports
                from invoice.models import Invoice
                
                # Find the invoice
                invoice = Invoice.objects.get(id=invoice_id)
                
                # Mark as havaleh generated
                invoice.havaleh_generated = True
                invoice.havaleh_date = timezone.now()
                invoice.havaleh_serial = serial
                invoice.save()
                
                # Log in comments field of the sale
                sale = invoice.sale
                havaleh_info = f"Havaleh created on {timezone.now()} with serial: {serial}"
                if sale.comments:
                    sale.comments += f"\n{havaleh_info}"
                else:
                    sale.comments = havaleh_info
                sale.save(update_fields=['comments'])
                
            except Exception as e:
                print(f"Error updating Invoice record: {e}")
                # Continue to generate PDF
        
        # Render the HTML template
        html_string = render_to_string('havaleh_pdf.html', context)
        
        # Create PDF with WeasyPrint
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        
        # Create a BytesIO object to store the PDF
        pdf_file = BytesIO()
        
        # Write the PDF to the BytesIO object
        html.write_pdf(pdf_file)
        
        # Get the value of the BytesIO object
        pdf_file.seek(0)
        pdf_content = pdf_file.getvalue()
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="havaleh_{serial}.pdf"'
        response['Content-Length'] = len(pdf_content)
        
        return response
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def havaleh_pdf(request):
    """Generate a PDF for the havaleh (delivery form)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is supported'}, status=405)
    
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Get all the form data
        date = data.get('date', '')
        serial = data.get('serial', '')
        items = data.get('items', [])
        note = data.get('note', '')
        invoice_id = data.get('invoice_id')
        
        # Process date using PersianDateText if available
        persian_date = date
        try:
            # Import here to avoid circular imports
            from invoice.utils import PersianDateText
            
            # Parse date if it's in format like "1403/03/15"
            if date and '/' in date:
                date_parts = date.split('/')
                if len(date_parts) == 3:
                    persian_date_obj = PersianDateText(date_parts)
                    persian_date = persian_date_obj.to_text()
        except Exception as e:
            print(f"Error processing Persian date: {e}")
            # Continue with original date
        
        # Calculate total weight and convert weights to Persian text
        total_weight = 0
        processed_items = []
        
        for item in items:
            weight = float(item.get('weight', 0))
            total_weight += weight
            
            # Create a copy of the item with Persian weight
            item_copy = item.copy()
            
            # Format weight with commas
            weight_persian = f"{weight:,.0f}"
            item_copy['weight_persian'] = weight_persian
            
            processed_items.append(item_copy)
        
        # Format total weight with Persian numerals
        total_weight_persian = f"{total_weight:,.0f}"
        
        # Prepare context for template
        context = {
            'date': date,
            'persian_date': persian_date,
            'serial': serial,
            'items': processed_items,
            'note': note,
            'total_weight': f"{total_weight:,.0f}",
            'total_weight_persian': total_weight_persian
        }
        
        # If invoice_id is provided, update the related Invoice record
        if invoice_id:
            try:
                # Import Invoice model here to avoid circular imports
                from invoice.models import Invoice
                
                # Find the invoice
                invoice = Invoice.objects.get(id=invoice_id)
                
                # Mark as havaleh generated
                invoice.havaleh_generated = True
                invoice.havaleh_date = timezone.now()
                invoice.havaleh_serial = serial
                invoice.save()
                
                # Log in comments field of the sale
                sale = invoice.sale
                havaleh_info = f"Havaleh created on {timezone.now()} with serial: {serial}"
                if sale.comments:
                    sale.comments += f"\n{havaleh_info}"
                else:
                    sale.comments = havaleh_info
                sale.save(update_fields=['comments'])
                
            except Exception as e:
                print(f"Error updating Invoice record: {e}")
                # Continue to generate PDF
        
        # Render the HTML template
        html_string = render_to_string('havaleh.html', context)
        
        # Create PDF with WeasyPrint - using basic settings compatible with all versions
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf_file = html.write_pdf(presentational_hints=True)
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="havaleh_{serial}.pdf"'
        
        return response
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def havaleh(request):
    """Render the havaleh page which will load the latest pending invoice"""
    return render(request, 'havaleh_page.html')

@csrf_exempt
def sales_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            current_time = datetime.now()
            jalali_datetime = jdatetime.datetime.fromgregorian(datetime=current_time)
            persian_date = jalali_datetime.strftime('%Y/%m/%d')
            total_amount = 0
            items = []
            for item in data.get('items', []):
                quantity = float(item.get('quantity', 0))
                price = float(item.get('price', 0))
                total = quantity * price
                items.append({
                    'description': item.get('description', ''),
                    'quantity': quantity,
                    'price': price,
                    'total': total
                })
                total_amount += total
            context = {
                'date': persian_date,
                'serial': data.get('serial', ''),
                'customer': data.get('customer', ''),
                'economic_code': data.get('economic_code', ''),
                'national_id': data.get('national_id', ''),
                'items': items,
                'total_amount': f"{total_amount:,.0f}",
                'note': data.get('note', ''),
            }
            html_string = render_to_string('sales_order.html', context)
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
            pdf = html.write_pdf()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=sales_order_{data.get("serial", "")}.pdf'
            return response
        except Exception as e:
            return JsonResponse({'error': f'Server Error: {str(e)}', 'status': 'error'}, status=500)


# New
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


@csrf_exempt
def latest_invoice(request):
    """Get the latest invoice from the database, regardless of status"""
    try:
        from invoice.models import Invoice
        
        # Get the latest invoice by creation date
        invoice = Invoice.objects.order_by('-created_at').first()
        
        if not invoice:
            return JsonResponse({'message': 'No invoices found'}, status=404)
        
        # Get the associated sale
        sale = invoice.sale
        
        # Prepare response data
        data = {
            'id': invoice.id,
            'sale_id': sale.id,
            'date': sale.date.isoformat() if sale.date else None,
            'customer_name': str(sale.customer_name),
            'invoice_number': getattr(sale, 'invoice_number', ''),
            'year': invoice.year,
            'month': invoice.month,
            'day': invoice.day,
            'is_paid': invoice.is_paid,
            'created_at': invoice.created_at.isoformat(),
            'list_of_reels': sale.list_of_reels,
            'width': sale.width,
            'net_weight': sale.net_weight
        }
        
        return JsonResponse(data)
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    

def get_next_sales_invoice(request):
    # You may want to filter by user: e.g. username=request.user.username
    sales = Sales.objects.filter(invoice_status="NA").order_by('date').first()
    if not sales:
        return JsonResponse({'error': 'No pending sales'}, status=404)
    # Serialize required fields
    data = {
        'id': sales.id,
        'customer_name': sales.customer_name,
        'license_number': sales.license_number,
        # ...add all fields you need for the invoice
        'items': [],  # If you have related items, serialize them too
    }
    return JsonResponse(data)

@csrf_exempt
def confirm_sales_invoice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sales_id = data.get('id')
        try:
            sales = Sales.objects.get(id=sales_id)
            if sales.invoice_status == "NA":
                sales.invoice_status = "Sent"
                sales.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Already confirmed.'}, status=400)
        except Sales.DoesNotExist:
            return JsonResponse({'error': 'Sales not found.'}, status=404)

def check_pending_invoice(request):

    """
    API endpoint to check if there's a pending invoice with 'NA' status.
    Returns JSON with:
    - has_pending: boolean indicating if a pending invoice exists
    - pending_id: ID of the pending invoice (if exists)
    """
    pending_invoice = Sales.objects.filter(invoice_status='NA').first()
    
    response_data = {
        'has_pending': pending_invoice is not None
    }
    
    if pending_invoice:
        response_data['pending_id'] = pending_invoice.id
    
    return JsonResponse(response_data)

@csrf_exempt
def get_last_10_sales(request):
    try:
        # Get last 10 sales ordered by date
        sales = Sales.objects.all().order_by('-date')[:10]
        sales_data = []

        for sale in sales:
            try:
                # Convert date to Jalali
                if isinstance(sale.date, datetime):
                    gregorian_date = sale.date
                    jdate = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
                    formatted_date = jdate.strftime('%Y/%m/%d')
                else:
                    formatted_date = str(sale.date)

                # Get customer details
                customer = sale.customer_name
                customer_name = str(getattr(customer, 'customer_name', '')) if hasattr(customer, 'customer_name') else str(customer)
                customer_economic_code = getattr(customer, 'economic_code', '') if hasattr(customer, 'economic_code') else ''
                customer_reg = getattr(customer, 'reg', '') if hasattr(customer, 'reg') else ''
                customer_national_id = getattr(customer, 'national_id', '') if hasattr(customer, 'national_id') else ''
                customer_postcode = getattr(customer, 'postcode', '') if hasattr(customer, 'postcode') else ''
                customer_address = getattr(customer, 'address', '') if hasattr(customer, 'address') else ''
                customer_phone = getattr(customer, 'phone', '') if hasattr(customer, 'phone') else ''

                # Get items from list_of_reels
                items = []
                total_weight = 0
                if sale.list_of_reels:
                    try:
                        reels_list = json.loads(sale.list_of_reels)
                        for reel in reels_list:
                            quantity = float(reel.get('quantity', 0))
                            total_weight += quantity
                            items.append({
                                'description': reel.get('description', ''),
                                'code': reel.get('code', ''),
                                'quantity': quantity,
                                'unit': reel.get('unit', 'kg'),
                                'price': float(reel.get('price', 0)),
                                'total': float(reel.get('total', 0))
                            })
                    except:
                        # If list_of_reels is not valid JSON, use net_weight
                        total_weight = float(getattr(sale, 'net_weight', 0))
                        items.append({
                            'description': getattr(sale, 'profile_name', ''),
                            'code': '',
                            'quantity': total_weight,
                            'unit': 'kg',
                            'price': float(getattr(sale, 'price_per_kg', 0)),
                            'total': float(getattr(sale, 'total_price', 0))
                        })

                sales_data.append({
                    'id': sale.id,
                    'date': formatted_date,
                    'serial': getattr(sale, 'invoice_number', ''),
                    'buyer_name': customer_name,
                    'buyer_economic_code': customer_economic_code,
                    'buyer_reg': customer_reg,
                    'buyer_national_id': customer_national_id,
                    'buyer_postcode': customer_postcode,
                    'buyer_address': customer_address,
                    'buyer_phone': customer_phone,
                    'items': items,
                    'total_amount': float(getattr(sale, 'total_price', 0)),
                    'total_items': len(items),
                    'total_weight': total_weight,
                    'profile_name': getattr(sale, 'profile_name', ''),
                    'width': float(getattr(sale, 'width', 0))
                })
            except Exception as e:
                print(f"Error processing sale {sale.id}: {str(e)}")
                continue

        return JsonResponse(sales_data, safe=False)

    except Exception as e:
        print(f"Error in get_last_10_sales: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)