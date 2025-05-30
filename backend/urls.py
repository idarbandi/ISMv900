from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp/", include('myapp.urls'), name='myapp'),
    path("invoice/", include('invoice.urls'), name='invoice'),
]
