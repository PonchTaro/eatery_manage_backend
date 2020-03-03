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
        fields = '__all__'
        depth = 1


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