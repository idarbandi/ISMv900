import graphene
from graphene_django import DjangoObjectType
from myapp.models import Truck, Driver, Shipment, Product, Customer
from invoice.models import Invoice

class TruckType(DjangoObjectType):
    class Meta:
        model = Truck
        fields = '__all__'

class DriverType(DjangoObjectType):
    class Meta:
        model = Driver
        fields = '__all__'

class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipment
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
        fields = '__all__'

class FilterInput(graphene.InputObjectType):
    invoice_status = graphene.String()
    truck_license_number = graphene.String()
    driver_name = graphene.String()
    shipment_status = graphene.String()
    shipment_type = graphene.String()
    shipment_invoice_status = graphene.String()
    supplier_name = graphene.String()
    product_status = graphene.String()
    customer_national_id = graphene.String() 