from django.contrib import admin

from eatery.eatery.models import Eatery, Product, Table, Voucher, BaseUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(BaseUser, UserAdmin)
# Register your models here.
admin.site.register(Eatery)
admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Voucher)
