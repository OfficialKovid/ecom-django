from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
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


# FOR ORDERS

@login_required(login_url='/login/')
def orders(request):
    # Retrieve orders associated with the current user
    user_orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {'user_orders': user_orders})

def order_it(request,product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request,'order.html',{'product': product})

@login_required(login_url='/login/')
def place_order(request):
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
	

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        total_price = product.price  # Assuming the total price is the price of the product

        # Assuming the user is authenticated, you can get the user instance
        user = request.user

        # Create address instance
        address_instance = Address.objects.create(
            user=user,
            address_line1=address,
            city=city,
            state=state,
            zip_code=postal_code,
            country=country
        )

        # Create order instance
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            status='Pending'  # You can set initial status as Pending or any other status
        )

        # Assuming you have a payment confirmation, you can update the payment status as well
        payment_status = 'Success'  # You need to retrieve this from your payment gateway response
        Payment.objects.create(
            order=order,
            payment_method='Cash on delivery',  # You can modify this based on the actual payment method
            amount_paid=total_price,
            transaction_id='',  # You can fill this with actual transaction ID if available
            status=payment_status
        )

        # You can add product to the order
        order.products.add(product)

        messages.success(request, 'Order placed successfully!')
        return redirect('/ecom/')  # Redirect to home page or any other page after successful order placement

    return render(request, 'order.html', {'product': product})