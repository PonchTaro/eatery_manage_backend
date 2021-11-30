from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from eatery_app.models import (
    Table,
    Product,
    Voucher,
    Eatery,
    ProductCategory,
)
from eatery_app.serializers import (
    TableSerializer,
    ProductSerializer,
    VoucherSerializer,
    EaterySerializer,
    OrderSerializer,
    ProductCategorySerializer,
)

class EateryViewSet(ModelViewSet):
    '''
    '''
    queryset = Eatery.objects.all()
    serializer_class = EaterySerializer

    @action(detail=True, methods=["GET"])
    def products(self, request, pk):
        instance = self.get_object()
        return Response(
            ProductSerializer(instance.product_set.all(), many=True).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["GET"])
    def categories(self, request, pk):
        instance = self.get_object()
        return Response(
            ProductCategorySerializer(instance.productcategory_set.all(), many=True).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["GET"])
    def tables(self, request, pk):
        eatery = self.get_object()
        data = TableSerializer(eatery.table_set.all(), many=True).data
        return Response(data)

    @action(detail=True, methods=["GET"], url_path='received-orders')
    def received_orders(self, request, pk):
        instance = self.get_object()
        pending_vouchers = Voucher.objects.filter(
            table__eatery=instance,
            status=Voucher.Status.PENDING
        )
        return Response()


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=["GET"], url_path='issue-code')
    def issue_code(self, request, pk=None):
        instance = self.get_object()
        serializer = TableSerializer(instance)
        data = serializer.issue_code()
        data['number'] = instance.number
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def occupy(self, request, pk=None):
        instance = self.get_object()
        if instance.is_available:
            serializer = TableSerializer(instance)
            serializer.occupy()
            return Response(
                serializer.context,
                status=status.HTTP_200_OK
            )
        newest_voucher = instance.voucher_set.order_by('-created').first()
        return Response({'voucher_id': newest_voucher.id}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def free(self, request, pk=None):
        instance = self.get_object()
        instance.free()
        return self.retrieve(request, pk)


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

# 管理画面で使う
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VoucherViewSet(ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

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
        serializer = VoucherSerializer(instance)
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
