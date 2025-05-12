from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Sales
from invoice.models import Invoice
from datetime import datetime

@receiver(pre_save, sender=Sales)
def create_invoice_on_status_change(sender, instance, **kwargs):
    """
    Signal handler to create an Invoice instance when a Sale's invoice_status
    changes from 'NA' to 'Sent'.
    """
    print(f"Signal triggered for sale {instance.id}: {instance.invoice_status}")
    
    try:
        # Check if this is a new object (no ID yet)
        if not instance.pk:
            print("New sale being created, skipping signal")
            return  # New object, skip
            
        # Get previous instance to check if status changed
        try:
            prev = Sales.objects.get(pk=instance.pk)
            print(f"Previous status: {prev.invoice_status}, New status: {instance.invoice_status}")
        except Sales.DoesNotExist:
            print("Could not find previous instance")
            return
            
        # Only proceed if status changed from 'NA' to 'Sent'
        if prev.invoice_status == "NA" and instance.invoice_status == "Sent":
            print(f"Status changed from NA to Sent for sale {instance.id}, creating invoice")
            
            # Check if an invoice already exists to avoid duplicates
            if Invoice.objects.filter(sale_id=instance.pk).exists():
                print(f"Invoice already exists for sale {instance.id}")
                return
                
            # Get the current date for the invoice
            date = instance.date or datetime.now()
            
            # Create the Invoice
            invoice = Invoice(
                sale=instance,
                year=date.year,
                month=date.month,
                day=date.day,
                customer=instance.customer_name if hasattr(instance.customer_name, 'id') else None,
                shipment=instance.shipment if hasattr(instance, 'shipment') else None
            )
            invoice.save()
            print(f"Invoice created successfully with ID: {invoice.id}")
    except Exception as e:
        import traceback
        print(f"Error in create_invoice_on_status_change signal: {e}")
        traceback.print_exc()