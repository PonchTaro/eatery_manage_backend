from io import BytesIO
from os import path
import base64
import qrcode
from django.urls import reverse
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from eatery_app.models import (
    Table,
    Product,
    Voucher,
    Eatery,
    Order,
    ProductCategory,
)

class EaterySerializer(ModelSerializer):
    class Meta:
        model = Eatery
        fields = [
            'id',
            'name',
            'address',
            'site_url',
            'tel',
            'tel2',
            'product_set',
            'table_set',
        ]
        extra_kwargs = {
            'product_set': {'read_only': True},
            'table_set': {'read_only': True},
        }


class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = [
            'id',
            'eatery',
            'number',
            'accomodation',
            'start_using_at',
            'status',
            'is_available',
            'is_reserved',
            'is_using',
        ]

    @staticmethod
    def _create_code_string(data):
        '''dataからQRコードを生成するメソッド'''
        code = qrcode.make(data)
        # TODO:(検討)生成したQRコードの画像をmediaに保存した後基礎情報を保存
        output_stream = BytesIO()
        code.save(output_stream)
        output_stream.seek(0)
        raw_data = output_stream.getvalue()
        return base64.b64encode(raw_data)

    def issue_code(self, data):
        '''テーブルのURLのQRコードを発行'''
        visit_url = path.join(
            settings.VISIT_URL.format(
                eatery_id=self.instance.eatery.id,
                table_id=self.instance.id
            ),
        )
        data['code'] = self._create_code_string(visit_url)
        data['type'] = 'image/png'
        return data 

    def occupy(self):
        '''テーブルを着席状態に書き換え & 請求書オブジェクトの作成'''
        self.instance.occupy()
        # 請求書のオブジェクトを作成
        voucher = Voucher.objects.create(table=self.instance)
        self.context['voucher_id'] = voucher.id
        return self.instance


class CreateBillSerializer(ModelSerializer):
    # 合計金額を確認する際などはこれを利用
    class Meta:
        model = Voucher
        fields = []

    def create_bill(self):
        # self.instanceはセットされている
        return self.instance.products.aggregate()


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'name',
            'eatery',
            'ordering'
        ]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['eatery'] = EaterySerializer(obj.eatery).data
        return data


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'eatery',
            'name',
            'price',
            'category',
            'icon',
            'image',
        ]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['category'] = {
            'id': obj.category.id,
            'name': obj.category.name,
            'ordering': obj.category.ordering
        }
        return data


class OrderSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'voucher',
            'number',
            'status',
        ]


class VoucherSerializer(ModelSerializer):
    # 作成だけでよいのでは
    class Meta:
        model = Voucher
        fields = '__all__'
        depth = 1

    def add_product(self, product, number):
        product = Product.objects.filter(id=product).first()
        if product is None:
            raise NotFound('注文された商品が存在しません')
        Order.objects.create(product=product, voucher=self.instance, number=number)
        return self.instance.products.all()