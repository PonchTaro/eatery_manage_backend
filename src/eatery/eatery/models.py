from django.db import models
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


class Product(ModelBase):
    name = models.CharField('商品名', max_length=512)
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=128)
    # フロントエンドで管理するのがめんどいのでアイコンのURLはsettings.pyのICON_URL参照
    icon = models.CharField(max_length=128)
    image = models.ImageField(blank=True)


class Table(ModelBase):
    class Status(models.IntegerChoices):
        AVAILABLE = 0, _('空き')
        RESERVED = 1, _('予約')
        USING = 2, _('使用中')
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    number = models.CharField(max_length=128, unique=True)
    accomodation = models.PositiveIntegerField()
    start_using_at = models.DateTimeField(verbose_name='使用開始時間')
    status = models.ImageField(
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    

class Invoice(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '請求'
    # TODO: 精算をする際にはTableが使用開始になった時間以降にcreateされた請求を集めてきて商品の合計金額を計算する
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    @property
    def total_price(self):
        '''紐づく商品の合計金額を返す'''
        pass


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
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        # 来客確認、キャンセル後はテーブルのステータスを戻す
        if instance.status in [Status.VISITED, Status.CANCELED]:
            instance.table.status = Table.Status.AVAILABLE
            instance.table.save()
        return instance



class Usage(ModelBase):
    pass