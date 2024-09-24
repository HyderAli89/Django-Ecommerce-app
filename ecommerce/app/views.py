from django.shortcuts import render
from django.views import View
from urllib import request
from django.http import HttpResponse
from . models import Product
from django.db.models import Count
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