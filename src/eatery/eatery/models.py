from django.db import models
from django.db.models import F, Sum
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class ModelBase(models.Model):
    class Meta:
        abstract = True
        ordering = [
            "-created",
        ]
    created = models.DateTimeField("作成日時", auto_now_add=True)
    updated = models.DateTimeField("更新日時", auto_now=True)
    enabled = models.BooleanField("有効", default=True)


class BaseUser(AbstractUser):
    class USER_TYPE(models.IntegerChoices):
        STAFF = 0, _('店員')
        STORE_MANAGER = 1, _('店長')
    user_type = models.IntegerField(
        choices=USER_TYPE.choices,
        default=USER_TYPE.STAFF
    )

    def __str__(self):
        return self.username


class Staff(BaseUser):
    def save(self, **kwargs):
        instance = super().save(commit=False)
        instance.user_type = BaseUser.USER_TYPE.STAFF
        return instance.save()


class StoreManger(BaseUser):
    def save(self, **kwargs):
        instance = super().save(commit=False)
        instance.user_type = BaseUser.USER_TYPE.STORE_MANAGER
        return instance.save()


class Eatery(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '飲食店'
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=1024)
    site_url = models.CharField(max_length=2048, blank=True)
    tel = models.CharField(max_length=128)
    tel2 = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.name}: {self.address}'


class ProductCategory(ModelBase):
    class Meta:
        unique_together = ['eatery', 'ordering']
    name = models.CharField(max_length=256)
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.eatery.name}: {self.name}'


class Product(ModelBase):
    class Meta:
        ordering = ['category__ordering']
    name = models.CharField('商品名', max_length=512)
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    # フロントエンドで管理するのがめんどいのでアイコンのURLはsettings.pyのICON_URL参照
    icon = models.CharField(max_length=128)
    image = models.ImageField(blank=True, null=True)


class Table(ModelBase):
    class Meta:
        ordering = ['number']
    class Status(models.IntegerChoices):
        AVAILABLE = 0, _('空き')
        RESERVED = 1, _('予約')
        USING = 2, _('使用中')
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(unique=True)
    accomodation = models.PositiveIntegerField()
    start_using_at = models.DateTimeField(verbose_name='使用開始時間', blank=True, null=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    @property
    def is_available(self):
        return self.status == Table.Status.AVAILABLE

    @property
    def is_reserved(self):
        return self.status == Table.Status.RESERVED

    @property
    def is_using(self):
        return self.status == Table.Status.USING

    def occupy(self):
        self.status = Table.Status.USING
        self.save()

    def reserve(self):
        self.status = Table.Status.RESERVED
        self.save()

    def free(self):
        self.status = Table.Status.AVAILABLE
        self.save()


class Voucher(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '伝票'
    class Status(models.IntegerChoices):
        PENDING = 0, _('未処理')
        CHECKED = 1, _('決済終了')
    # TODO: 精算をする際にはTableが使用開始になった時間以降にcreateされた請求を集めてきて商品の合計金額を計算する
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Order', blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    @property
    def total_price(self):
        '''紐づく商品の合計金額を返す'''
        return self.order_set.annotate(
            subtotal=F('product__price') * F('number')
        ).aggregate(sum=Sum('subtotal'))['sum']


class Order(ModelBase):
    class Status(models.IntegerChoices):
        PENDING = 0, _('未処理')
        SERVED = 1, _('配膳済み')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(verbose_name="注文数", default=1)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)


class Reservation(ModelBase):
    class Status(models.IntegerChoices):
        READY = 0, _('待ち')
        VISITED = 1, _('来店確認完了')
        CANCELED = 2, _('キャンセル')
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    responder = models.ForeignKey(Staff, on_delete=models.PROTECT)
    reserved_date = models.DateField(verbose_name='予約日')
    reserved_time = models.TimeField(verbose_name='予約時刻')
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.READY
    )
    # 予約客情報
    name = models.CharField(max_length=1024)
    tel = models.CharField(max_length=128)
    # 請求書は先に作成する
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        # 来客確認、キャンセル後はテーブルのステータスを戻す
        if instance.status in [Status.VISITED, Status.CANCELED]:
            instance.table.status = Table.Status.AVAILABLE
            instance.table.save()
        return instance



class Usage(ModelBase):
    pass