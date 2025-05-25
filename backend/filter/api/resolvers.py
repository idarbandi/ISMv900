import graphene
from django.db.models import Q
from .types import (
    TruckType, DriverType, SupplierType,
    InvoiceType, InvoiceItemType, FilterInput
)
from myapp.models import Truck, Driver, Supplier, Invoice, InvoiceItem

class FilterQuery(graphene.ObjectType):
    filtered_data = graphene.List(graphene.JSONString, input=FilterInput(required=True))

    def resolve_filtered_data(self, info, input):
        model_name = input.model
        filters = input.filters

        model_map = {
            'truck': Truck,
            'driver': Driver,
            'supplier': Supplier,
            'invoice': Invoice,
            'invoice_item': InvoiceItem
        }

        if model_name not in model_map:
            raise Exception(f"Invalid model name: {model_name}")

        model = model_map[model_name]
        query = Q()

        for field, value in filters.items():
            if value:
                if isinstance(value, str):
                    query &= Q(**{f"{field}__icontains": value})
                else:
                    query &= Q(**{field: value})

        results = model.objects.filter(query)
        return [obj.to_dict() for obj in results] 