from django.urls import path
from .views import *


urlpatterns = [
path('', homePageView, name='home'),
path('ecom/',ecom, name = 'ecom'),
path('shop/',shop, name = 'shop'),
path('haircare/',haircare, name = 'haircare'),
path('makeup/',makeup, name = 'makeup'),
path('skincare/',skincare, name = 'skincare'),
path('signup/',signup, name = 'signup'),
path('login/',login_page, name = 'login'),
path('logout/',logout_user, name = 'logout'),
path('account/',account, name = 'account'),
path('orders/',orders, name = 'orders'),
path('product/<int:product_id>/', product_detail, name='product_detail'),

]