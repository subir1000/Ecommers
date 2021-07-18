from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(UserDetail)
admin.site.register(AddToCartTable)
admin.site.register(Order_Product)
admin.site.register(Order_product_detail)