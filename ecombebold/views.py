from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# from django.http import HttpResponse
def homePageView(request):
	return redirect("/ecom/")

def ecom(request):
	return render(request,"index.html")


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})


def signup(request):
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")

		user = User.objects.filter(username = username)
		if user.exists():
			messages.info(request,'Username already exist')
			return redirect('/signup/')

		user = User.objects.create(
			email=email,
			username=username
		)
		user.set_password(password)
		user.save()
		return redirect('/login/')
	return render(request,"signup.html") 

def login_page(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		if not User.objects.filter(username = username).exists():
			messages.info(request,'Wrong Username')
			return redirect('/login/')
			
		user = authenticate(username = username, password = password)
		if user is None:
			messages.error(request,'Wrong Passward')
			return redirect('/login/')
		else:
			login(request,user)
			return redirect('/account/')

	return render(request,"login.html")

@login_required(login_url='/login/')
def account(request):
	return render(request,"account.html")

@login_required(login_url='/account/')
def orders(request):
	return render(request,"orders.html")

def logout_user(request):
	logout(request)
	return redirect('/login/')


# FOR SHOP ALL
products = Product.objects.all()
dic = {'products': products}

def shop(request):
	return render(request,"shop.html",context=dic)


# FOR HAIR
hair_care_category = Category.objects.get(name='Hair Care')
haircare = Product.objects.filter(category=hair_care_category) # Retrieve all products belonging to the hair care category
hair={'haircare': haircare}

def haircare(request):
	return render(request,"haircare.html",context=hair)


# FOR MAKEUP
makeup_category = Category.objects.get(name='Make Up')
makeup = Product.objects.filter(category=makeup_category) # Retrieve all products belonging to the hair care category
make={'makeup': makeup}
def makeup(request):
	return render(request,"makeup.html",context=make)



# FOR SKIN CARE
skin_care_category = Category.objects.get(name='Skin Care')
skincare = Product.objects.filter(category=skin_care_category) # Retrieve all products belonging to the hair care category
skin={'skincare': skincare}
def skincare(request):
	return render(request,"skincare.html",context=skin)
