from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
# Create your views here.

from django.contrib.auth import authenticate,logout,login
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import *
from .models import *
from django.contrib.auth.models import User
from datetime import date,timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

def MyCartData(user):
    cartlist = []
    if user.is_authenticated:
        cart = AddToCartTable.objects.filter(usr = user)[::-1]
        cartlist = cart[:2]
    return cartlist


def AllCategory():
    allcat = Category.objects.all()
    return allcat

def Send_mail(user,order_id):
    checkout_detail = Order_Product.objects.get(id = order_id)
    Totalprice = 0
    product_detail = Order_product_detail.objects.filter(order_detail = checkout_detail)
    for i in product_detail:
        Totalprice+=i.totalprice
    name = user.first_name
    to_email = user.email
    from_email = settings.EMAIL_HOST_USER
    sub = 'Confirmation Mail'
    msg = EmailMultiAlternatives(sub,' ',from_email,[to_email])
    d = {"name":name,"product_detail":product_detail,"Totalprice":Totalprice}
    html = get_template('mail.html').render(d)
    msg.attach_alternative(html,'text/html')
    msg.send()



def Home(request):
    #Send_mail(request.user,1)
    d = {"allcat":AllCategory(),"mycartdata":MyCartData(request.user)}
    return render(request,'index.html',d)


def AboutUs(request):
    d = {"allcat": AllCategory(),"mycartdata":MyCartData(request.user)}
    return render(request,'about.html',d)

def ContactUs(request):
    d = {"allcat": AllCategory(),"mycartdata":MyCartData(request.user)}
    return render(request,'contact.html',d)

def Login(request):
    error = False
    if request.method  == "POST":
        dic = request.POST
        u = dic['user']
        p =  dic['pwd']
        user = authenticate(username = u,password = p)
        if user:
            login(request,user)
            return redirect('home')
        else:
            error = True

    d = {"allcat": AllCategory(),"error":error,"mycartdata":MyCartData(request.user)}
    return render(request,'login.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Signup(request):
    error = False
    if request.method  == "POST":
        dic = request.POST
        u = dic['user']
        p =  dic['pwd']
        f = dic['fname']
        l = dic['lname']
        e = dic['email']
        m = dic['mob']
        a = dic['add']
        i = request.FILES['img']
        userdata = User.objects.filter(username = u)
        if not userdata:
            user = User.objects.create_user(username=u,password=p,email=e,first_name = f,last_name = l)
            UserDetail.objects.create(usr = user,image = i,mobile = m,address = a)
            return redirect('login')
        else:
            error = True
    d = {"allcat": AllCategory(),"error":error,"mycartdata":MyCartData(request.user)}
    return render(request,'signin.html',d)

def ShopList(request,sid):
    subcatdata = SubCategory.objects.get(id = sid)
    allpro = Product.objects.filter(subcat = subcatdata)
    paginator = Paginator(allpro,2)
    page = request.GET.get('page',1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    othersubcat = SubCategory.objects.filter(cat = subcatdata.cat)
    d = {"allcat": AllCategory(),"allpro":products,"othersubcat":othersubcat,"mycartdata":MyCartData(request.user)}
    return render(request,'shop.html',d)


def Product_details(request,pid):
    prodata = Product.objects.get(id = pid)
    subcat = prodata.subcat
    related_pro = Product.objects.filter(subcat = subcat)[:4]
    sizelist = []
    if prodata.size:
        sizelist = prodata.size.split(',')

    d = {"allcat": AllCategory(),"prodata":prodata,
         "related_pro":related_pro,"sizelist":sizelist
         ,"mycartdata":MyCartData(request.user)}
    return render(request,'product-single.html',d)


def Add_To_Cart(request,pid):
    prodata = Product.objects.get(id = pid)
    user = request.user
    cartdata = AddToCartTable.objects.filter(usr = user,pro=prodata).first()
    if request.method == "POST":
        q = request.POST['quantity']
        s = ''
        if prodata.size:
            s = request.POST['size']
        total = int(prodata.price) * int(q)
        if cartdata:
            cartdata.quantity += int(q)
            cartdata.TotalPrice += total
            cartdata.save()
        else:
            AddToCartTable.objects.create(pro = prodata,usr=user,
                                          quantity = q,TotalPrice = total,
                                          size = s)
    return redirect('mycart')


def MyCart(request):
    cartdata = AddToCartTable.objects.filter(usr = request.user)
    total = 0
    for i in cartdata:
        total += i.TotalPrice
    d = {"allcat": AllCategory(),
         "mycartdata":MyCartData(request.user),
         "cartdata":cartdata,"total":total}
    return render(request,'cart.html',d)


def Remove_Pro_from_cart(request,cid):
    data = AddToCartTable.objects.get(id = cid)
    data.delete()
    return redirect('mycart')

headers = { "X-Api-Key": "api-key",
            "X-Auth-Token": "auth-token"}

import requests
import json
#pip install requests
def Payment(user,amount,order_id):
    payload = {
        "purpose":"Product payment",
        "buyer_name":user.username,
        "amount":10,
        "email":user.email,
        "phone":user.mobile,
        "send_email":True,
        "send_sms":True,
        "redirect_url":"http://127.0.0.1:8000/payment_check/"+str(order_id)+"/"

    }
    url = "https://www.instamojo.com/api/1.1/payment-requests/"
    response = requests.post(url,data=payload,headers=headers)
    print(response)
    res = response.text
    y = json.loads(res)
    payment_id = y['payment_request']['id']
    long_url = y['payment_request']['longurl']

    return payment_id,long_url


def Payment_check(request,order_id):
    order_data = Order_Product.objects.get(id = order_id )
    payment_id = order_data.payment_id
    url = "https://www.instamojo.com/api/1.1/payment-requests/" + str(payment_id) + "/"
    response = requests.get(url,headers=headers)
    res = response.text
    y = json.loads(res)
    print(y)
    status = y['payment_request']['status']
    d = {"order_data": order_data, "status": status}
    if status == "Completed":
        user = request.user
        Send_mail(user,order_id)
        order_data.payment_status = "Done"
        order_data.save()
        pro_ordered_data  = Order_product_detail.objects.filter(order_detail = order_data)
        for i in pro_ordered_data:
            i.status = 'Order Confirmed'
            i.save()
            prodata = Product.objects.get(id = i.pro.id)
            q = i.quantity
            prodata.stock -= q
            prodata.save()
            cart = AddToCartTable.objects.filter(usr = request.user,pro = i.pro)
            cart.delete()

        return render(request,'confirmation.html',d)
    else:
        return render(request,'confirmation.html',d)


import random
def Checkout(request,cid):
    form = OrderForm()
    if cid != 'All':
        cartdata = AddToCartTable.objects.filter(id = cid)
    elif cid == 'All':
        cartdata = AddToCartTable.objects.filter(usr = request.user)
    totalpayamount = 0
    for i in cartdata:
        totalpayamount += i.TotalPrice
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.save()
            data.usr = request.user
            data.amount = totalpayamount
            ran = random.randint(100000,999999)
            data.order_id = ran
            data.orderdate = date.today()
            data.save()
            payid,long_url = Payment(request.user,totalpayamount,data.id)
            data.payment_id = payid
            data.save()
            expdate = date.today() + timedelta(5)
            for i in cartdata:
                Order_product_detail.objects.create(order_detail = data,pro = i.pro,
                                                    quantity = i.quantity,
                                                    totalprice =i.TotalPrice,
                                                    expected_date = expdate)


            return redirect(long_url)

    d = {"form": form,"cartdata":cartdata,"Grand_total":totalpayamount}

    return render(request,'checkout.html',d)
#user.set_password(new)
#user.save()


def UserDashboard(request,type):
    c1 = ''
    c2 = ''
    c3 = ''
    c4 = ''
    allorder  = []
    pending_order = []
    checkout_detail = []
    profile_detail = []
    order_data = Order_Product.objects.filter(usr=request.user)
    for checkout in order_data:
        alldata = Order_product_detail.objects.filter(order_detail=checkout)
        for i in alldata:
            if i.status == 'Delivered':
                allorder.append(i)
            else:
                pending_order.append(i)

    if type == 'AllOrder':
        c1 = 'active'

    elif type == 'PendingOrder':
        c2 = 'active'

    elif type == 'AddressList':
        c3 = 'active'
        checkout_detail = Order_Product.objects.filter(usr = request.user)

    elif type == 'Profile':
        profile_detail = UserDetail.objects.filter(usr = request.user).first()
        c4 = 'active'
    else:
        raise Http404()
    d = {"type":type,"class1":c1,"class2":c2,"class3":c3,"class4":c4
         ,"data":allorder,"data1":pending_order,"checkout_detail":checkout_detail,
         "profile_detail":profile_detail}
    return render(request,'dashboard.html',d)


def Track_Order(request,oid):
    data = Order_product_detail.objects.get(id = oid)
    d = {"data":data}
    return render(request,'track.html',d)


def Add_Product(request):
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.save()
            return redirect('shop',data.subcat.id)
    d = {'form':form,"name":"Add New","name1":"Add"}
    return render(request,'add_edit_product.html',d)


def Edit_Product(request,pid):
    prodata = Product.objects.get(id = pid)
    form = AddProductForm(instance=prodata)
    if request.method == "POST":
        form = AddProductForm(request.POST or None, request.FILES or None,instance=prodata)
        if form.is_valid():
            data = form.save()
            return redirect('pdetail',pid)
    d = {'form':form,"prodata":prodata,"name":"Edit: "+prodata.name,"name1":"Edit"}
    return render(request, 'add_edit_product.html',d)


def Delete_Details(request,data_id,type):
    if type == 'Category':
        data = Category.objects.get(id = data_id)
        data.delete()

    elif type == 'SubCategory':
        data = SubCategory.objects.get(id=data_id)
        data.delete()
    elif type == 'Product':
        data = Product.objects.get(id=data_id)
        data.delete()
    else:
        raise Http404()
    return redirect('home')

def Completed_Order(request):
    data = Order_product_detail.objects.filter(status = 'Delivered')
    d = {"data":data}
    return render(request,'order.html',d)

def Pending_Order(request):
    data = []
    all_order = Order_product_detail.objects.all()
    for i in all_order:
        if i.status != 'Delivered':
            data.append(i)
    d = {"data":data}
    return render(request,'pending_order.html',d)

def Change_status(request,order_id):
    status = ["Order Confirmed", 'Shipped', 'Out For Delivery','Delivered']
    order_data = Order_product_detail.objects.get(id = order_id)
    ind = status.index(order_data.status)
    dropdown = status[ind:]
    if request.method == "POST":
        s = request.POST['status']
        order_data.status = s
        order_data.save()
        ind = status.index(order_data.status)
        dropdown = status[ind:]
        return redirect('pending')

    d = {"data": order_data,"dropdown":dropdown}


    return render(request,'change_status.html',d)







