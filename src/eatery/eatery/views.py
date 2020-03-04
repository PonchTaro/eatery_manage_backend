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

    @action(detail=True, methods=["GET"])
    def products(self, request, pk):
        eatery = self.get_object()
        data = ProductSerializer(eatery.product_set.all(), many=True).data,
        return Response(
            data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["GET"])
    def tables(self, request, pk):
        eatery = self.get_object()
        data = TableSerializer(eatery.table_set.all(), many=True).data
        return Response(data)


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=["POST"])
    def use(self, request, pk=None):
        instance = self.get_object()
        instance.occupy()
        return self.retrieve(request, pk)

    @action(detail=True, methods=["POST"])
    def free(self, request, pk=None):
        instance = self.get_object()
        instance.free()
        return self.retrieve(request, pk)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

