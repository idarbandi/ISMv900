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
        fields = (
            'id', 'reel_number', 'width', 'gsm', 'length', 'grade',
            'breaks', 'status', 'location', 'receive_date', 'last_date',
            'profile_name', 'qr_code', 'comments'
        )

    # Convert snake_case to camelCase
    reel_number = graphene.String(source='reel_number')
    receive_date = graphene.DateTime(source='receive_date')
    last_date = graphene.DateTime(source='last_date')
    profile_name = graphene.String(source='profile_name')
    qr_code = graphene.String(source='qr_code')

class ShipmentType(DjangoObjectType):
    class Meta:
        model = Shipments
        fields = ('id', 'shipment_type')

class FilterInput(graphene.InputObjectType):
    startDate = graphene.Date()
    endDate = graphene.Date()
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
    # Product specific filters
    productReelNumber = graphene.String()
    productWidth = graphene.Int()
    productGsm = graphene.Int()
    productLength = graphene.Int()
    productGrade = graphene.String()
    productStatus = graphene.String()
    productLocation = graphene.String()
    productProfileName = graphene.String()
    minBreaks = graphene.Int()
    maxBreaks = graphene.Int()

# Define the Union type
class FilterResultUnion(graphene.Union):
    class Meta:
        types = (TruckType, SalesType, CustomerType, ProductType, ShipmentType)

class Query(graphene.ObjectType):
    filteredData = graphene.List(FilterResultUnion, filterInput=graphene.Argument(FilterInput))
    # Add a direct products query for debugging
    products = graphene.List(ProductType)

    def resolve_products(self, info):
        return Products.objects.all()

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

        # Product filtering
        product_filter = Q()
        if filterInput:
            # Filter by reel number
            if filterInput.productReelNumber:
                product_filter &= Q(reel_number__icontains=filterInput.productReelNumber)
            
            # Filter by width
            if filterInput.productWidth:
                product_filter &= Q(width=filterInput.productWidth)
            
            # Filter by GSM
            if filterInput.productGsm:
                product_filter &= Q(gsm=filterInput.productGsm)
            
            # Filter by length
            if filterInput.productLength:
                product_filter &= Q(length=filterInput.productLength)
            
            # Filter by grade
            if filterInput.productGrade:
                product_filter &= Q(grade__icontains=filterInput.productGrade)
            
            # Filter by status
            if filterInput.productStatus:
                product_filter &= Q(status=filterInput.productStatus)
            
            # Filter by location
            if filterInput.productLocation:
                product_filter &= Q(location__icontains=filterInput.productLocation)
            
            # Filter by profile name
            if filterInput.productProfileName:
                product_filter &= Q(profile_name__icontains=filterInput.productProfileName)
            
            # Filter by breaks range
            if filterInput.minBreaks is not None:
                product_filter &= Q(breaks__gte=filterInput.minBreaks)
            if filterInput.maxBreaks is not None:
                product_filter &= Q(breaks__lte=filterInput.maxBreaks)
            
            # Filter by date range
            if filterInput.startDate:
                product_filter &= Q(receive_date__gte=filterInput.startDate)
            if filterInput.endDate:
                product_filter &= Q(receive_date__lte=filterInput.endDate)

        # Apply product filters if any exist
        if product_filter:
            products = Products.objects.filter(product_filter)
            queryset.extend(list(products))
        else:
            # If no filters are applied, return all products
            products = Products.objects.all()
            queryset.extend(list(products))

        return queryset

schema = graphene.Schema(query=Query) 