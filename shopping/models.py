from django.db import models
from django.contrib.auth.models import User
# Create your models here.
status = [["Order Confirmed","Order Confirmed"],
        ['Shipped','Shipped'],
        ['Out For Delivery','Out For Delivery'],
        ['Delivered','Delivered'],
        ]


class Category(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    cat = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cat.name + '--' + self.name

class Product(models.Model):
    subcat = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    img1 = models.FileField(null=True)
    img2 = models.FileField(null=True)
    img3 = models.FileField(null=True)
    des = models.TextField(null=True)
    size = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.subcat.name + '--' + self.name


class UserDetail(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile =  models.CharField(max_length=100,null=True)
    image =  models.FileField(null=True)
    address = models.TextField(null = True)

    def __str__(self):
        return self.usr.username


class AddToCartTable(models.Model):
    pro = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    usr = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)
    TotalPrice = models.IntegerField(null=True)
    size = models.CharField(max_length=100,null=True,blank = True)

class Order_Product(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    fullname =  models.CharField(max_length=100,null=True)
    houes_no = models.CharField(max_length=100,null=True,blank=True)
    area_name = models.CharField(max_length=100,null=True)
    city_state = models.CharField(max_length=100,null=True)
    landmark = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length=100,null=True)
    mobile1 = models.CharField(max_length=100,null=True)
    mobile2 = models.CharField(max_length=100,null=True)
    payment_status = models.CharField(max_length=100,default="Not Done")
    payment_id = models.CharField(max_length=500,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    orderdate = models.DateField(null=True,blank=True)


    def __str__(self):
        return self.fullname


class Order_product_detail(models.Model):
    order_detail = models.ForeignKey(Order_Product,on_delete=models.CASCADE,null = True)
    pro = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True)
    totalprice = models.IntegerField(null=True)
    expected_date = models.DateField(null=True)
    status = models.CharField(max_length=100, null=True, choices=status, blank=True)





