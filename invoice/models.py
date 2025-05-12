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
    sale = models.OneToOneField(Sales, on_delete=models.CASCADE, related_name='invoice')
    
    # Invoice date components (for easier filtering/searching)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    
    # When the invoice was created
    created_at = models.DateTimeField(default=timezone.now)
    
    # Status fields
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Optional foreign keys (can be null if the relation doesn't exist)
    customer = models.ForeignKey('myapp.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    shipment = models.ForeignKey('myapp.Shipments', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'Invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"Invoice #{self.id} for Sale #{self.sale_id} ({self.created_at.strftime('%Y-%m-%d')})"




