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


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1