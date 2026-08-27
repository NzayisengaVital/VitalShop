from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name = 'home'),
path('about/', views.about, name ='about'),
path('product/<int:product_id>/', views.product_detail, name='product_detail'),
path(
    'cart/add/<int:product_id>/',
    views.add_to_cart,
    name='add_to_cart'
),
path(
    'cart/',
    views.cart,
    name='cart'
),
path(
    'cart/increase/<int:product_id>/',
    views.increase_quantity,
    name='increase_quantity'
),

path(
    'cart/decrease/<int:product_id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),

path(
    'cart/remove/<int:product_id>/',
    views.remove_from_cart,
    name='remove_from_cart'
),
path(
    'checkout/',
    views.checkout,
    name='checkout'
),
path(
    'order/success/<int:order_id>/',
    views.order_success,
    name='order_success'
),
path(
    'order/track/',
    views.track_order,
    name='track_order'
),
path(
    'login/',
    views.login_view,
    name='login'
),

path(
    'register/',
    views.register_view,
    name='register'
),

path(
    'account/',
    views.account,
    name='account'
),

path(
    'logout/',
    views.logout_view,
    name='logout'
),
path(
    'my-orders/',
    views.my_orders,
    name='my_orders'
),
path(
    'privacy/',
    views.privacy,
    name='privacy'
),

path(
    'terms/',
    views.terms,
    name='terms'
),
path(
    'contact/',
    views.contact,
    name='contact'
),
path(
    'help/',
    views.help_center,
    name='help'
),
]