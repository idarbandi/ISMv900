from django.db import models
from django.utils import timezone
from myapp.models import Sales

class Invoice(models.Model):
    """
    Model representing an invoice generated when a sale is confirmed.
    
    This model is automatically created via a signal when a Sales instance
    has its invoice_status changed from 'NA' to 'Sent'.
    """
    # Link to the original sale
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True, blank=True)
    
    # Invoice date components (for easier filtering/searching)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    
    # When the invoice was created
    created_at = models.DateTimeField(default=timezone.now)
    
    # Status fields
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Havaleh (delivery form) tracking fields
    havaleh_generated = models.BooleanField(default=False)
    havaleh_date = models.DateTimeField(null=True, blank=True)
    havaleh_serial = models.CharField(max_length=255, null=True, blank=True)
    
    # Optional foreign keys (can be null if the relation doesn't exist)
    customer = models.ForeignKey('myapp.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    # OneToOneField relationship with Shipments
    shipment = models.OneToOneField('myapp.Shipments', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')
    
    class Meta:
        db_table = 'Invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"Invoice #{self.id} for Sale #{self.sale_id} ({self.created_at.strftime('%Y-%m-%d')})"


class Havaleh(models.Model):
    """
    Model representing a delivery form (Havaleh) generated for invoices.
    Tracks items that are being delivered based on an invoice.
    """
    # Link to the invoice
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='havaleh')
    
    # Havaleh details
    date = models.DateTimeField(default=timezone.now)
    serial = models.CharField(max_length=255, unique=True)
    note = models.TextField(blank=True, null=True)
    
    # When the Havaleh was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Havaleh'
        verbose_name = 'Havaleh'
        verbose_name_plural = 'Havalehs'
    
    def __str__(self):
        return f"Havaleh #{self.serial} for Invoice #{self.invoice_id}"


class HavalehItem(models.Model):
    """
    Model representing individual items in a Havaleh (delivery form).
    """
    # Link to the Havaleh
    havaleh = models.ForeignKey(Havaleh, on_delete=models.CASCADE, related_name='items')
    
    # Item details
    name = models.CharField(max_length=255)
    gsm = models.CharField(max_length=50, blank=True, null=True)
    width = models.CharField(max_length=50, blank=True, null=True)
    buyer = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    weight = models.FloatField(default=0)
    
    class Meta:
        db_table = 'HavalehItem'
        verbose_name = 'Havaleh Item'
        verbose_name_plural = 'Havaleh Items'
    
    def __str__(self):
        return f"{self.name} - {self.weight}kg ({self.havaleh.serial})" 