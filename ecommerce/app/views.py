from django.shortcuts import render,redirect
from django.views import View
from urllib import request
from django.http import HttpResponse,JsonResponse
from . models import Customer, Product,Cart,Payment,OrderPlaced
from django.db.models import Count,Q
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages 
# Create your views here.
def home(request):
    return render(request,"app/home.html")
def about(request):
    return render(request,"app/about.html")
def contact(request):
    return render(request,"app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product= Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals()) # locals is built in function to pass the value from request to html file

class CategoryTitle(View):
    def get(self,request,val):
        product= Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetails(View):
    def get(self,request,pk):
        product= Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())

# customer registration views
class CustomerRegistrationView(View):
    def get(self,request):
        form= CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully")
        else:
            messages.warning(request,"Invalid Input Data") 
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    # after login it will redirect it to login page
    def get(self,request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # getting all data and storing it in variable's
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile= form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile save Successfully")
        else:
            messages.warning(request,"invalid Input Data")
        return render(request,'app/profile.html',locals())
    
def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk) # when we click on update the data will be fetch here 
        form=CustomerProfileForm(instance=add) # the fetch data will be automattically to text 
        return  render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get("prod_id")
    product= Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user 
    cart=Cart.objects.filter(user=user)
    amount = 0 
    for p in cart:
        value= p.quantity*p.product.discounted_price
        amount=amount + value
    totalamount=amount + 40
    
    return render (request, 'app/addtocart.html',locals())

def orders(request):
    
     order_id=request.GET.get('order_id')
     cust_id=request.GET.get('cust_id')
     #print("payment done: oid",order_id," pid,payment_id," cid",cust_id)
     user = request.user
     #return redirect("orders")
    #  customer=Customer.objects.get(id=cust_id) #To update payment status and payment id payment-Payment.objects.get(razorpay_order_id-order_id)

     #To save order details
     cart=Cart.objects.filter(user=user)
     for c in cart:
         OrderPlaced(user=user, product=c.product, quantity=c.quantity).save()
        #c.delete()
     order_placed=OrderPlaced.objects.filter(user=user)
     return render(request,"app/orders.html",locals())

class checkout(View):
    def get(self,request):
        user=request.user
        # add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
       
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount + value
        totalamount= famount +  40
        payment= Payment(
        user=user,
        amount=totalamount,
        )
        payment.save()  
       
       
       # for order placed
        
        
        # user = request.user
        # #return redirect("orders")
        # customer=Customer.objects.get(user=user) #To update payment status and payment id payment-Payment.objects.get(razorpay_order_id-order_id)
        # Payment.save()
        # #To save order details
        # cart=Cart.objects.filter(user=user)
        # for c in cart:
        #     OrderPlaced(user=user, customer=customer[0], product=cart_items, quantity=c.quantity).save()
        # c.delete()
        
        return render(request, 'app/checkout.html',locals())

def status(request):
    return render(request,"app/status.html")

def payment_done(request):
     order_id=request.GET.get('order_id')
     cust_id=request.GET.get('cust_id')
     #print("payment done: oid",order_id," pid,payment_id," cid",cust_id)
     user = request.user
     #return redirect("orders")
     customer=Customer.objects.get(id=cust_id) #To update payment status and payment id payment-Payment.objects.get(razorpay_order_id-order_id)
     Payment.save()
     #To save order details
     cart=Cart.objects.filter(user=user)
     for c in cart:
         OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
     c.delete()
     return redirect("orders")


def plus_cart(request):
    #   if request.method == 'GET':
    #       prod_id = request.GET.get('prod_id')
    #       c=Cart.objects.filter(Q(product=prod_id) &Q(user=request.user))  # Q is required for multiple condition
    #       c.quantity+=1
    #       c.save() # Saving the cart
          
    #       # again getting data of cart objects
    #       user = request.user
    #       cart = Cart.objects.filter(user=user)
    #       amount = 0 
    #       for p in cart:
    #          value= p.quantity*p.product.discounted_price
    #          amount=amount + value
    #       totalamount=amount + 40
    
    #       data={
    #           'quantity':c.quantity,
    #           'amount':amount,
    #           'totalamount': totalamount            
    #       }
    #       return JsonResponse(data)
    
    
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if prod_id is missing
        if prod_id:
            try:
                # Use filter() instead of get() to handle multiple objects
                cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
                if cart_items.exists():
                    # If multiple cart entries exist, decide how to handle them (e.g., take the first or merge quantities)
                    c = cart_items.first()  # Get the first cart entry (can modify to handle multiple if needed)
                    c.quantity += 1
                    c.save()  # Save the updated cart item
    
                    # Recalculate the total amount for the cart
                    user = request.user
                    cart = Cart.objects.filter(user=user)
                    amount = 0 
                    for p in cart:
                        value = p.quantity * p.product.discounted_price
                        amount += value
                    totalamount = amount + 40  # Shipping cost or fixed charge
    
                    data = {
                        'quantity': c.quantity,
                        'amount': amount,
                        'totalamount': totalamount
                    }
                    return JsonResponse(data)
                else:
                    return JsonResponse({'error': 'Cart entry not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'prod_id missing in GET parameters'}, status=400)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if prod_id is missing
        if prod_id:
            try:
                # Use filter() instead of get() to handle multiple objects
                cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
                if cart_items.exists():
                    # If multiple cart entries exist, decide how to handle them (e.g., take the first or merge quantities)
                    c = cart_items.first()  # Get the first cart entry (can modify to handle multiple if needed)
                    c.quantity -= 1
                    c.save()  # Save the updated cart item
    
                    # Recalculate the total amount for the cart
                    user = request.user
                    cart = Cart.objects.filter(user=user)
                    amount = 0 
                    for p in cart:
                        value = p.quantity * p.product.discounted_price
                        amount += value
                    totalamount = amount + 40  # Shipping cost or fixed charge
    
                    data = {
                        'quantity':c.quantity,
                        'amount': amount,
                        'totalamount': totalamount
                    }
                    return JsonResponse(data)
                else:
                    return JsonResponse({'error': 'Cart entry not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'prod_id missing in GET parameters'}, status=400)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        if prod_id:
            try:
                # Filter by the product and user
                cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
                if cart_items.exists():
                    # Delete the item(s) from the cart
                    cart_items.delete()

                    # Recalculate the total amount for the cart
                    user = request.user
                    cart = Cart.objects.filter(user=user)
                    amount = 0
                    for p in cart:
                        value = p.quantity * p.product.discounted_price
                        amount += value
                    totalamount = amount + 40  # Assuming 40 is the shipping cost or fixed charge

                    data = {
                        'amount': amount,
                        'totalamount': totalamount
                    }
                    return JsonResponse(data)
                else:
                    return JsonResponse({'error': 'Cart entry not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'prod_id missing in GET parameters'}, status=400)

