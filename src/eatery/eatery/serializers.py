from io import BytesIO
from os import path
import base64
import qrcode
from django.urls import reverse
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from eatery.eatery.models import (
    Table,
    Product,
    Invoice,
    Eatery,
    Order,
)

class EaterySerializer(ModelSerializer):
    class Meta:
        model = Eatery
        fields = '__all__'
        depth = 1


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
    def create_code_string(data):
        '''
        QRコードを生成する
        '''
        code = qrcode.make(data)
        # TODO:(検討)生成したQRコードの画像をmediaに保存した後基礎情報を保存
        output_stream = BytesIO()
        code.save(output_stream)
        output_stream.seek(0)
        raw_data = output_stream.getvalue()
        return base64.b64encode(raw_data)

    def occupy(self):
        self.instance.occupy()
        # 請求書のオブジェクトを作成
        invoice = Invoice.objects.create(table=self.instance)
        invoice_url = path.join(
            settings.TOP_URL.format(
                eatery_id=self.instance.eatery.id,
                invoice_id=invoice.id
            ),
        )
        # 請求書のIDを埋め込んだURLをQRコード化
        self.context['code'] = self.create_code_string(invoice_url)
        self.context['type'] = 'image/png'
        self.context['invoice_id'] = invoice.id
        return self.instance


class CreateBillSerializer(ModelSerializer):
    # 合計金額を確認する際などはこれを利用
    class Meta:
        model = Invoice
        fields = []

    def create_bill(self):
        # self.instanceはセットされている
        return self.instance.products.aggregate()

class InvoiceQRIssueSerialier(ModelSerializer):
    class Meta:
        model = Invoice
        fields = []

    def issue_invoice_qr(self):
        # invoiceのURLを取ってきてQRコードを作成
        pass


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


class OrderSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'invoice',
            'number',
        ]


class InvoiceSerializer(ModelSerializer):
    # 作成だけでよいのでは
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1

    def add_product(self, product, number):
        product = Product.objects.filter(id=product).first()
        if product is None:
            raise NotFound('注文された商品が存在しません')
        Order.objects.create(product=product, invoice=self.instance, number=number)
        return self.instance.products.all()