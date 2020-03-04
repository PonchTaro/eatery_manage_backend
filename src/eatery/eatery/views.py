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
    OrderSerializer,
)

class EateryViewSet(ModelViewSet):
    queryset = Eatery.objects.all()
    serializer_class = EaterySerializer

    @action(detail=True, methods=["GET"])
    def products(self, request, pk):
        eatery = self.get_object()
        return Response(
            ProductSerializer(eatery.product_set.all(), many=True).data,
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
        serializer = TableSerializer(instance)
        serializer.occupy()
        return Response(
            serializer.context,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["POST"])
    def free(self, request, pk=None):
        instance = self.get_object()
        instance.free()
        return self.retrieve(request, pk)



# 管理画面で使う
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=["GET"])
    def table(self, request, pk=None):
        '''どのテーブルが紐づいているか'''
        instance = self.get_object()
        return Response(
            TableSerializer(instance.table).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=["GET"])
    def products(self, request, pk):
        eatery = self.get_object()
        return Response(
            ProductSerializer(eatery.product_set.all(), many=True).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["POST"], url_path='add-product')
    def add_product(self, request, pk=None):
        instance = self.get_object()
        serializer = InvoiceSerializer(instance)
        ordered_products = serializer.add_product(**request.data)
        return Response(
            ProductSerializer(ordered_products, many=True).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=["GET"])
    def orders(self, request, pk=None):
        instance = self.get_object()
        return Response(
            OrderSerializer(instance.order_set.all(), many=True).data,
            status=status.HTTP_200_OK
        )
