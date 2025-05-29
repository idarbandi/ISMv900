import graphene
from graphene_django import DjangoObjectType
from myapp.models import Purchases
from django.db.models import Q

class PurchaseType(DjangoObjectType):
    class Meta:
        model = Purchases
        fields = (
            'id', 'date', 'status', 'receiveDate', 'paymentDate',
            'licenseNumber', 'materialType', 'materialName', 'supplierName',
            'unit', 'quantity', 'quality', 'penalty', 'weight1', 'weight2',
            'netWeight', 'pricePerKg', 'vat', 'totalPrice', 'extraCost',
            'invoiceStatus', 'paymentDetails', 'invoiceNumber', 'documentInfo',
            'comments', 'cancellationReason', 'username', 'logs'
        )

    # Convert snake_case to camelCase
    receive_date = graphene.DateTime(source='receiveDate')
    payment_date = graphene.DateTime(source='paymentDate')
    license_number = graphene.String(source='licenseNumber')
    material_type = graphene.String(source='materialType')
    material_name = graphene.String(source='materialName')
    supplier_name = graphene.String(source='supplierName')
    price_per_kg = graphene.BigInt(source='pricePerKg')
    total_price = graphene.BigInt(source='totalPrice')
    extra_cost = graphene.BigInt(source='extraCost')
    invoice_status = graphene.String(source='invoiceStatus')
    payment_details = graphene.String(source='paymentDetails')
    invoice_number = graphene.String(source='invoiceNumber')
    document_info = graphene.String(source='documentInfo')
    cancellation_reason = graphene.String(source='cancellationReason')

class PurchaseFilterInput(graphene.InputObjectType):
    startDate = graphene.Date()
    endDate = graphene.Date()
    status = graphene.String()
    licenseNumber = graphene.String()
    materialType = graphene.String()
    materialName = graphene.String()
    supplierName = graphene.String()
    weight1 = graphene.Int()
    weight2 = graphene.Int()
    netWeight = graphene.Int()
    pricePerKg = graphene.Int()
    totalPrice = graphene.Int()
    extraCost = graphene.Int()
    invoiceStatus = graphene.String()
    paymentStatus = graphene.String()

class PurchaseQuery(graphene.ObjectType):
    purchases = graphene.List(PurchaseType)
    filteredPurchases = graphene.List(PurchaseType, filterInput=graphene.Argument(PurchaseFilterInput))

    def resolve_purchases(self, info):
        return Purchases.objects.all()

    def resolve_filteredPurchases(self, info, filterInput=None):
        queryset = Purchases.objects.all()
        
        if filterInput:
            # Start with an empty Q object for combined filtering
            combined_filter = Q()

            # Filter by status
            if filterInput.status:
                combined_filter &= Q(status=filterInput.status)

            # Filter by license number
            if filterInput.licenseNumber:
                combined_filter &= Q(license_number__icontains=filterInput.licenseNumber)

            # Filter by material
            if filterInput.materialType:
                combined_filter &= Q(material_type__icontains=filterInput.materialType)
            if filterInput.materialName:
                combined_filter &= Q(material_name__icontains=filterInput.materialName)

            # Filter by supplier
            if filterInput.supplierName:
                combined_filter &= Q(supplier_name__icontains=filterInput.supplierName)

            # Filter by weights
            if filterInput.weight1:
                combined_filter &= Q(weight1=filterInput.weight1)
            if filterInput.weight2:
                combined_filter &= Q(weight2=filterInput.weight2)
            if filterInput.netWeight:
                combined_filter &= Q(net_weight=filterInput.netWeight)

            # Filter by prices
            if filterInput.pricePerKg:
                combined_filter &= Q(price_per_kg=filterInput.pricePerKg)
            if filterInput.totalPrice:
                combined_filter &= Q(total_price=filterInput.totalPrice)
            if filterInput.extraCost:
                combined_filter &= Q(extra_cost=filterInput.extraCost)

            # Filter by statuses
            if filterInput.invoiceStatus:
                combined_filter &= Q(invoice_status=filterInput.invoiceStatus)
            if filterInput.paymentStatus:
                combined_filter &= Q(status=filterInput.paymentStatus)

            # Filter by date range
            if filterInput.startDate:
                combined_filter &= Q(date__gte=filterInput.startDate)
            if filterInput.endDate:
                combined_filter &= Q(date__lte=filterInput.endDate)

            queryset = queryset.filter(combined_filter)

        return queryset 