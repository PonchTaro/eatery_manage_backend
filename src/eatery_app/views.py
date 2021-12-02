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
    '''店舗のリソースを管理するAPI
    '''
    queryset = Eatery.objects.all()
    serializer_class = EaterySerializer

    @action(detail=True, methods=["GET"])
    def products(self, request, pk):
        '''特定の店舗が売っている商品一覧を返す'''
        instance = self.get_object()
        data = ProductSerializer(instance.product_set.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def categories(self, request, pk):
        '''特定の店舗が売っている商品のカテゴリ一覧を返す'''
        instance = self.get_object()
        data = ProductCategorySerializer(instance.productcategory_set.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def tables(self, request, pk):
        '''特定の店舗が持っているテーブル一覧を返す'''
        eatery = self.get_object()
        data = TableSerializer(eatery.table_set.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='received-orders')
    def received_orders(self, request, pk):
        '''特定の店舗が現在抱えている注文一覧を返す処理'''
        # FIXME: 
        # 単一のAPIで全ての店舗の注文のリクエストを捌くのは頭悪い
        # 特にこの処理はリアルタイム性が求められる
        # 業務時間中のトランザクションは店舗ごとに処理して
        # 1日に1回程度メインのDBと同期取るような設計にしたい？
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
        '''テーブルに対応するQRコードを発行する'''
        instance = self.get_object()
        serializer = TableSerializer(instance)
        data = {}
        data = serializer.issue_code(data)
        data['number'] = instance.number
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def occupy(self, request, pk=None):
        '''客がテーブルに着席する際の処理'''
        instance = self.get_object()
        # 空いているなら請求書を発行する
        if instance.is_available:
            serializer = TableSerializer(instance)
            serializer.occupy()
            return Response(
                serializer.context,
                status=status.HTTP_200_OK
            )
        # 予約中なら先に請求書は作成されているので、その情報を返す
        # NOTE: なぜ先に請求書を作成していたのか忘れた
        newest_voucher = instance.voucher_set.order_by('-created').first()
        # FIXME: 他の客が使用している場合に注文ができてしまう
        return Response({'voucher_id': newest_voucher.id}, status=status.HTTP_200_OK)

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
