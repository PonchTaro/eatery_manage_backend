from django.db import models

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
    icon = models.CharField(max_length=128)
    image = models.ImageField(blank=True)


class Table(ModelBase):
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE)
    number = models.CharField(max_length=128, unique=True)
    accomodation = models.PositiveIntegerField()


class Invoice(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '請求'
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)



class Usage(ModelBase):
    pass