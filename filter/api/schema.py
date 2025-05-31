import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from myapp.models import Customer, Products, Sales, Shipments, Truck, Purchases
from django.db.models import Q
from .purchases import PurchaseType, PurchaseFilterInput, PurchaseQuery

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
        fields = (
            'id', 'date', 'status', 'location', 'receive_date', 'entry_time',
            'weight1_time', 'weight2_time', 'exit_time', 'shipment_type',
            'license_number', 'customer_name', 'supplier_name', 'weight1',
            'unload_location', 'unit', 'quantity', 'quality', 'penalty',
            'weight2', 'net_weight', 'list_of_reels', 'profile_name', 'width',
            'sales_id', 'price_per_kg', 'total_price', 'extra_cost',
            'material_type', 'material_name', 'vat', 'invoice_status',
            'payment_status', 'document_info', 'comments', 'cancellation_reason',
            'username', 'logs'
        )

    # Convert snake_case to camelCase
    receive_date = graphene.DateTime(source='receive_date')
    entry_time = graphene.DateTime(source='entry_time')
    weight1_time = graphene.DateTime(source='weight1_time')
    weight2_time = graphene.DateTime(source='weight2_time')
    exit_time = graphene.DateTime(source='exit_time')
    shipment_type = graphene.String(source='shipment_type')
    license_number = graphene.String(source='license_number')
    customer_name = graphene.String(source='customer_name')
    supplier_name = graphene.String(source='supplier_name')
    unload_location = graphene.String(source='unload_location')
    list_of_reels = graphene.String(source='list_of_reels')
    profile_name = graphene.String(source='profile_name')
    sales_id = graphene.Int(source='sales_id')
    price_per_kg = graphene.BigInt(source='price_per_kg')
    total_price = graphene.BigInt(source='total_price')
    extra_cost = graphene.BigInt(source='extra_cost')
    material_type = graphene.String(source='material_type')
    material_name = graphene.String(source='material_name')
    invoice_status = graphene.String(source='invoice_status')
    payment_status = graphene.String(source='payment_status')
    document_info = graphene.String(source='document_info')
    cancellation_reason = graphene.String(source='cancellation_reason')

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
    productWidth = graphene.List(graphene.String)
    productGsm = graphene.Int()
    productLength = graphene.Int()
    productGrade = graphene.String()
    productStatus = graphene.String()
    productLocation = graphene.List(graphene.String)
    productProfileName = graphene.String()
    minBreaks = graphene.Int()
    maxBreaks = graphene.Int()
    # Shipment specific filters
    shipmentStatus = graphene.String()
    shipmentLocation = graphene.String()
    licenseNumber = graphene.String()
    customerName = graphene.String()
    weight1 = graphene.Int()
    weight2 = graphene.Int()
    netWeight = graphene.String()
    materialType = graphene.String()
    materialName = graphene.String()
    pricePerKg = graphene.Int()
    totalPrice = graphene.Int()
    extraCost = graphene.Int()
    invoiceStatus = graphene.String()
    paymentStatus = graphene.String()
    unloadLocation = graphene.String()

# Define the Union type
class FilterResultUnion(graphene.Union):
    class Meta:
        types = (TruckType, SalesType, CustomerType, ProductType, ShipmentType)

class Query(PurchaseQuery, graphene.ObjectType):
    filteredData = graphene.List(FilterResultUnion, filterInput=graphene.Argument(FilterInput))
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
                product_filter &= Q(width__in=filterInput.productWidth)
            
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
                location_filter = Q()
                for location in filterInput.productLocation:
                    location_filter |= Q(location=location)
                product_filter &= location_filter
            
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

        # Shipment filtering
        shipment_filter = Q()
        if filterInput:
            # Filter by shipment type
            if filterInput.shipmentType:
                shipment_filter &= Q(shipment_type=filterInput.shipmentType)
            
            # Filter by status
            if filterInput.shipmentStatus:
                shipment_filter &= Q(status=filterInput.shipmentStatus)
            
            # Filter by location
            if filterInput.shipmentLocation:
                shipment_filter &= Q(location__icontains=filterInput.shipmentLocation)
            
            # Filter by license number
            if filterInput.licenseNumber:
                shipment_filter &= Q(license_number__icontains=filterInput.licenseNumber)
            
            # Filter by customer name
            if filterInput.customerName:
                shipment_filter &= Q(customer_name__icontains=filterInput.customerName)
            
            # Filter by supplier name
            if filterInput.supplierName:
                shipment_filter &= Q(supplier_name__icontains=filterInput.supplierName)
            
            # Filter by weights
            if filterInput.weight1:
                shipment_filter &= Q(weight1=filterInput.weight1)
            if filterInput.weight2:
                shipment_filter &= Q(weight2=filterInput.weight2)
            if filterInput.netWeight:
                shipment_filter &= Q(net_weight=filterInput.netWeight)
            
            # Filter by material
            if filterInput.materialType:
                shipment_filter &= Q(material_type__icontains=filterInput.materialType)
            if filterInput.materialName:
                shipment_filter &= Q(material_name__icontains=filterInput.materialName)
            
            # Filter by prices
            if filterInput.pricePerKg:
                shipment_filter &= Q(price_per_kg=filterInput.pricePerKg)
            if filterInput.totalPrice:
                shipment_filter &= Q(total_price=filterInput.totalPrice)
            if filterInput.extraCost:
                shipment_filter &= Q(extra_cost=filterInput.extraCost)
            
            # Filter by statuses
            if filterInput.invoiceStatus:
                shipment_filter &= Q(invoice_status=filterInput.invoiceStatus)
            if filterInput.paymentStatus:
                shipment_filter &= Q(payment_status=filterInput.paymentStatus)

            # Filter by unload location
            if filterInput.unloadLocation:
                shipment_filter &= Q(unload_location__icontains=filterInput.unloadLocation)

            # Filter by date range
            if filterInput.startDate:
                shipment_filter &= Q(date__gte=filterInput.startDate)
            if filterInput.endDate:
                shipment_filter &= Q(date__lte=filterInput.endDate)

        # Apply shipment filters if any exist
        if shipment_filter:
            shipments = Shipments.objects.filter(shipment_filter)
            queryset.extend(list(shipments))
        else:
            # If no filters are applied, return all shipments
            shipments = Shipments.objects.all()
            queryset.extend(list(shipments))

        return queryset

schema = graphene.Schema(query=Query) 