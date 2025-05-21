import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from myapp.models import Customer, Products, Sales, Shipments, Truck

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class TruckType(DjangoObjectType):
    class Meta:
        model = Truck
        fields = ('id', 'license_number', 'driver_name')

class SalesType(DjangoObjectType):
    class Meta:
        model = Sales
        fields = ('id', 'total_price')

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'customer_name', 'national_id')

class ProductType(DjangoObjectType):
    class Meta:
        model = Products
        fields = ('id', 'profile_name')

class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipments
        fields = ('id', 'shipment_type')

class FilterInput(graphene.InputObjectType):
    start_date = graphene.Date()
    end_date = graphene.Date()
    customer = graphene.ID()
    product = graphene.ID()
    shipment = graphene.ID()
    truck_license_number = graphene.String()
    driver_name = graphene.String()
    shipment_type = graphene.String()
    supplier_name = graphene.String()
    customer_national_id = graphene.String()
    min_amount = graphene.Float()
    max_amount = graphene.Float()

# Define the Union type
class FilterResultUnion(graphene.Union):
    class Meta:
        types = (TruckType, SalesType, CustomerType, ProductType, ShipmentType)

class Query(graphene.ObjectType):
    filteredData = graphene.List(FilterResultUnion, filterInput=graphene.Argument(FilterInput))

    def resolve_filteredData(self, info, filterInput=None):
        # For testing, return some dummy Django model instances
        return [
            Truck(
                pk=1,
                license_number="123ABC",
                driver_name="John Doe"
            ),
            Shipments(
                pk=1,
                shipment_type="Incoming",
            ),
            Products(
                pk=1,
                profile_name="Test Product",
            ),
            Customer(
                pk=1,
                customer_name="Test Customer",
                national_id="1234567890"
            ),
            Sales(
                pk=1,
                total_price=1000.00
            )
        ]

schema = graphene.Schema(query=Query) 