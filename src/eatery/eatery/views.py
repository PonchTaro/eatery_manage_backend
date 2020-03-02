from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from eatery.eatery.models import (
    Table,
    Product,
    Invoice,
    Eatery,
)
from eatery.eatery.serializers import (
    TableSerializer,
    ProductSerializer,
    InvoiceSerializer,
    EaterySerializer,
)

class EateryViewSet(ModelViewSet):
    queryset = Eatery.objects.all()
    serializer_class = EaterySerializer

    @action(detail=True)
    def products(self, request, pk):
        eatery = self.get_object()
        return Response(
            ProductSerializer(eatery.product_set.all(), many=True).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True)
    def tables(self, request, pk):
        eatery = self.get_object()
        return Response(
            eatery.table_set.values('id', 'number', 'accomodations')
        )
    

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    
