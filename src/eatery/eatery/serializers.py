from io import BytesIO
from os import path
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
    def create_code(data):
        '''
        QRコードを生成する
        '''
        code = qrcode.make(data)
        # TODO:(検討)生成したQRコードの画像をmediaに保存した後基礎情報を保存
        output_stream = BytesIO()
        code.save(output_stream)
        output_stream.seek(0)
        return output_stream

    def occupy(self):
        self.instance.occupy()
        # 請求書のオブジェクトを作成
        invoice = Invoice.objects.create(table=self.instance)
        invoice_url = path.join(
            settings.HOST_URL,
            reverse('invoice-detail', args=[invoice.id])[1:]
        )
        # 請求書のIDを埋め込んだURLをQRコード化
        self.context['code'] = self.create_code(invoice_url)
        self.context['invoice_id'] = invoice.id
        return self.instance



class CreateBillSerializer(ModelSerializer):
    # 合計金額を確認する際などはこれを利用
    class Meta:
        model = Table
        fields = []

    def create_bill(self):
        # self.instanceはセットされている
        total_price = 0
        invoices = Invoice.objects.filter(
            table=self.instance,
            created__gte=self.instance.start_using_at
        )
        for i in invoices:
            total_price += i.total_price
        return total_price


class InvoiceQRIssueSerialier(ModelSerializer):
    class Meta:
        model = Invoice

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


class InvoiceSerializer(ModelSerializer):
    # 作成だけでよいのでは
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1

    def create(self, validted_data):
        # TODO: レコードを作成した後にQRコードを発行
        pass