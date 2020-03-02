from django.contrib import admin

from eatery.eatery.models import Eatery, Product, Table, Invoice
# Register your models here.
admin.site.register(Eatery)
admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Invoice)
