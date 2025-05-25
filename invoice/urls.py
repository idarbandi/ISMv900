from django.urls import path
from .views import *
from invoice.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("api/havaleh-pdf/", havaleh, name='havaleh-pdf'),

    path("invoice/", invoice_page),
    path("invoice/sales_order/", sales_order),
    path("invoice/havaleh", havaleh),
    path("api/get_last_10_sales/", get_last_10_sales, name='get_last_10_sales'),

    # path("api/sales-order-pdf/", sales_order, name='sales-order-pdf'),
    # path("test-api/", lambda request: render(request, 'test_api.html')),
    # path("api/latest-invoice/", latest_invoice),
]