from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart,Payment,OrderPlaced,Category
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
# Create your views here.
@login_required
def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    category=[]
    category.append(Category.objects.get(title='Books'))
    category.append(Category.objects.get(title='Electronics'))
    category.append(Category.objects.get(title="MenClothings"))
    return render(request,'app/home.html',locals())

@login_required
def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())

@login_required
def contact(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryViews(View):
    def get(self,request,val):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        category=Category.objects.get(title=val)
        product=Product.objects.filter(category=category)

        paginator = Paginator(product, 25) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'app/category.html',locals())

@login_required
def allcategory(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 9) # Show 9 category per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'app/categoryall.html',locals())

    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"congrats!! User created successfully")
        else:
            messages.warning(request,"Invalid Input data")
        return render(request,"app/customerregistration.html",locals())  

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,"app/profile.html",locals())    
        
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,locality=locality,city=city
            ,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congrats!! Profile Saved successfully")
        else:
            messages.warning(request,"Invalid Input data")
        return render(request,"app/profile.html",locals())    

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/address.html",locals())    
    
@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,"app/updateAddress.html",locals())    

    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']

            add.save()
            messages.success(request,"congrats!! Profile Update successfully")
        else:
            messages.warning(request,"Invalid Input data")
        return redirect("address")

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    c=Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
    if(c is False):
        print("None")
        Cart(user=user,product=product).save()
    else:
        cart=Cart.objects.get(Q(product=product) & Q(user=request.user))
        cart.quantity+=1
        cart.save()
        print("update")
        
    return redirect("/cart")

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount+=value
    totalamount=amount+40
    return render(request,'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_item=Cart.objects.filter(user=user)
        famount=0
        for p in cart_item:
            value=p.quantity*p.product.discounted_price
            famount+=value
        totalamount=famount+40
        # razoramount=int(totalamount*100)
        # client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        # data={'amount':razoramount,"currency":"INR","receipt":"order_rcptid_11"}
        # payment_response=client.order.create(data=data)
        # print(payment_response)
        # order_id=payment_response['id']
        # order_status=payment_response['status']
        # if order_status=='created':
        #     payment=Payment(
        #         user=user,
        #         amount=totalamount,
        #         razorpay_order_id=order_id,
        #         razorpay_payment_status=order_status
        #     )
        #     payment.save()
        return render(request,'app/checkout.html',locals())

@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    # payment=Payment.objects.get(razorpay_order_id=order_id)
    # payment.paid=True
    # payment.razorpay_payment_id=payment_id
    # payment.save()
    # cart=Cart.objects.filter(user=user)
    # for c in cart:
    #     OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,
    #     payment=payment).save()

    #     c.delete()
    return redirect("order")

@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())


def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # print(vars(c))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if(c.quantity==1):
            c.delete()
        else:
            c.quantity-=1
            c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        quantity=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
            quantity+=p.quantity
        totalamount=amount+40
        data={
            'quantity':quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        quantity=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
            quantity+=p.quantity
        totalamount=amount+40
        data={
            'quantity':quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

@login_required
def search(request):
    query=request.GET['search']
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,'app/search.html', locals())