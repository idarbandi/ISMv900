from django.db import models
from invoice.utils import PersianDateText
from myapp.models import Customer, Shipments

class Invoice(models.Model):
    queue = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    shipment = models.ForeignKey(Shipments, on_delete=models.CASCADE, related_name='invoices')
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    @property
    def persian_date_text(self):
        return PersianDateText([self.year, self.month, self.day]).to_text()
    
    @property
    def persian_price(self):
        """
        Returns the price in Persian words.
        """
        return words(self.price_in_numbers)




