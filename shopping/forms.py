from django import forms
from .models import *
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order_Product
        #fields = '__all__'
        exclude = ['usr','payment_status','amount','payment_id','order_id','orderdate']

        widgets = {
            "fullname":forms.TextInput(attrs={"placeholder":"FullName","class":"form-control"}),
            "houes_no": forms.TextInput(attrs={"placeholder": "House Number", "class": "form-control"}),
            "area_name": forms.TextInput(attrs={"placeholder": "Area Name", "class": "form-control"}),
            "city_state": forms.TextInput(attrs={"placeholder": "City/State", "class": "form-control"}),
            "landmark": forms.TextInput(attrs={"placeholder": "Landmark", "class": "form-control"}),
            "pincode": forms.TextInput(attrs={"placeholder": "Pincode", "class": "form-control"}),
            "mobile1": forms.TextInput(attrs={"placeholder": "Mobile Number", "class": "form-control"}),
            "mobile2": forms.TextInput(attrs={"placeholder": "Alternate Mobile Number", "class": "form-control"}),

        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            "subcat":forms.Select(attrs={"class":"form-control"}),
            "name":forms.TextInput(attrs={"placeholder":"Product Name","class":"form-control"}),
            "price": forms.NumberInput(attrs={"placeholder": "Price", "class": "form-control"}),
            "stock": forms.NumberInput(attrs={"placeholder": "Product Stock", "class": "form-control"}),
            "img1": forms.FileInput(attrs={"class": "form-control"}),
            "img2": forms.FileInput(attrs={"class": "form-control"}),
            "img3": forms.FileInput(attrs={"class": "form-control"}),
            "des": forms.Textarea(attrs={"placeholder": "Description", "class": "form-control"}),
            "size": forms.TextInput(attrs={"placeholder": "Size (if required)", "class": "form-control"}),

        }
