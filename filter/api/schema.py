import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from myapp.models import Customer, Products, Sales, Shipments, Truck
from django.db.models import Q

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class TruckType(DjangoObjectType):
    class Meta:
        model = Truck
        fields = '__all__' # Include all fields from the Truck model

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
    truckLicenseNumber = graphene.String()
    driverName = graphene.String()
    shipmentType = graphene.String()
    supplierName = graphene.String()
    customerNationalId = graphene.String()
    minAmount = graphene.Float()
    maxAmount = graphene.Float()

# Define the Union type
class FilterResultUnion(graphene.Union):
    class Meta:
        types = (TruckType, SalesType, CustomerType, ProductType, ShipmentType)

class Query(graphene.ObjectType):
    filteredData = graphene.List(FilterResultUnion, filterInput=graphene.Argument(FilterInput))

    def resolve_filteredData(self, info, filterInput=None):
        queryset = []

        # Start with an empty Q object for combined filtering
        combined_filter = Q()

        # Filter Trucks by license number
        if filterInput and filterInput.truckLicenseNumber:
            combined_filter |= Q(license_number__icontains=filterInput.truckLicenseNumber)

        # Filter Trucks by driver name
        if filterInput and filterInput.driverName:
            combined_filter |= Q(driver_name__icontains=filterInput.driverName)

        # Apply the combined filter to the Truck model
        if combined_filter:
             trucks = Truck.objects.filter(combined_filter)
             queryset.extend(list(trucks))

        # TODO: Implement filtering for other models and combine the results

        return queryset

schema = graphene.Schema(query=Query) 