"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shopping.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name = 'home'),
path('AboutUs/',AboutUs,name = 'about'),
path('ContactUs',ContactUs,name = 'contact'),
path('Login/',Login,name = 'login'),
path('Logout/',Logout,name = 'logout'),
path('Signup/',Signup,name = 'signup'),
path('Product_List/<int:sid>/',ShopList,name = 'shop'),
path('Product_detail/<int:pid>/',Product_details,name = 'pdetail'),
path('Add_to_cart/<int:pid>/',Add_To_Cart,name = 'add_to_cart'),
path('MYCart/',MyCart,name = 'mycart'),
path('Remove_product/<int:cid>/',Remove_Pro_from_cart,name = 'remove'),
path('Order_Product/<str:cid>/',Checkout,name = 'checkout'),
path('payment_check/<int:order_id>/',Payment_check,name = 'payment_check'),
path('Dashboard/<str:type>',UserDashboard,name = 'dashboard'),
path('Track_order/<int:oid>',Track_Order,name = 'track'),
path('Add_Product/',Add_Product,name = 'add_pro'),
path('edit_Product/<int:pid>/',Edit_Product,name = 'edit_pro'),
path('Delete_details/<int:data_id>/<str:type>',Delete_Details,name = 'delete'),
path('Completed_Order_list/',Completed_Order,name = 'completed'),
path('Pending_Order_list/',Pending_Order,name = 'pending'),
path('Change_status/<int:order_id>/',Change_status,name = 'change'),

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
