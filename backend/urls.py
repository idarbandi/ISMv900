from django.contrib import admin
from django.urls import path, include
from invoice.views import sales_order, latest_pending_sale, test_api, confirm_sales_invoice, simple_latest_pending_sale

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp/", include('myapp.urls'), name='myapp'),
    path("api/sales-order-pdf/", sales_order, name='sales-order-pdf'), #changes by darbandi
    path("api/latest-pending-sale/", latest_pending_sale), #changes by darbandi
    path("api/test-endpoint/", test_api), #added test endpoint
    path("api/simple-latest-pending-sale/", simple_latest_pending_sale), #added simple version
    path("api/confirm-sales-invoice/<int:sales_id>/", confirm_sales_invoice), #added confirmation endpoint
]
