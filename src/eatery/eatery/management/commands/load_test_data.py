from random import randint
from django.core.management.base import BaseCommand, CommandError
from eatery.eatery.models import (
    Eatery, Table, Product, Order, ProductCategory, Voucher
)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('eatery_name')

    def handle(self, *args, **options):
        name = options['eatery_name']
        e = Eatery.objects.create(name=name, tel='09-0000-0000')
        # テーブル作成
        for i in range(1, 13):
            Table.objects.create(number=i, accomodation=4, eatery=e)
        # 商品作成
        data = {
            ('local_drink', '飲み物'): [
                ('生ビール(中)', 298),
                ('ハイボール', 298),
                ('レモンサワー', 320),
                ('はちみつレモン', 320),
                ('烏龍茶', 250),
            ],
            ('restaurant', 'スピードメニュー'): [
                ('たこわさ', 510),
                ('たこ焼き', 500),
                ('ポテト', 500),
                ('キムチ', 280),
                ('チャンジャ', 520),
                ('なめこ', 500)
            ]
        }
        for i, (info, values) in enumerate(data.items(), start=1):
            c = ProductCategory.objects.create(
                name=info[1],
                ordering=i, 
                eatery=e
            )
            for v in values:
                Product.objects.create(
                    name=v[0],
                    price=v[1],
                    category=c,
                    eatery=e,
                    icon=info[0]
                )
        # 伝票の作成
        t = Table.objects.first()
        v = Voucher.objects.create(table=t)
        # 商品の注文
        randomized_products = Product.objects.order_by('?')[:3]
        for p in randomized_products:
            Order.objects.create(
                voucher=v,
                product=p,
                number=randint(1, 3)
            )