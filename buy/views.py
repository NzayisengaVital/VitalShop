from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import (
    ContactMessage,
    Category,
    Product,
    OrderItem,
    Order

    )
# Create your views here.
def home(request):

    products = Product.objects.filter(
        available=True
    ).order_by('-created_at')

    categories = Category.objects.all()

    # Search
    search_query = request.GET.get('search', '').strip()

    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    # Category filter
    category_id = request.GET.get('category', '').strip()

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    # Price filters
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
            'search_query': search_query,
            'selected_category': category_id,
            'min_price': min_price,
            'max_price': max_price,
        }
    )

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
        }
    )
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            available=True
        )

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        delivery_address = request.POST.get('delivery_address')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            delivery_address=delivery_address,
            total_amount=total
)

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Empty cart after successful order
        request.session['cart'] = {}
        request.session.modified = True

        return redirect(
            'order_success',
            order_id=order.id
        )

    return render(
        request,
        'checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        'order_success.html',
        {
            'order': order,
        }
    )
def track_order(request):

    order = None
    error = None

    if request.method == 'POST':

        order_id = request.POST.get('order_id', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not order_id or not phone:

            error = "Please enter both your order number and phone number."

        else:

            try:

                order = Order.objects.get(
                    id=order_id,
                    phone=phone
                )

            except Order.DoesNotExist:

                error = "No order was found with those details."

    return render(
        request,
        'track_order.html',
        {
            'order': order,
            'error': error,
        }
    )
def login_view(request):

    if request.user.is_authenticated:
        return redirect('account')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('account')

        error = 'Invalid username or password.'

    return render(
        request,
        'login.html',
        {
            'error': error
        }
    )

def register_view(request):

    if request.user.is_authenticated:
        return redirect('account')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password:

            error = 'Please fill in all fields.'

        elif password != password2:

            error = 'Passwords do not match.'

        elif User.objects.filter(username=username).exists():

            error = 'This username is already taken.'

        elif User.objects.filter(email=email).exists():

            error = 'This email is already registered.'

        else:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect('account')

    return render(
        request,
        'register.html',
        {
            'error': error
        }
    )
@login_required
def account(request):

    return render(
        request,
        'account.html'
    )
def logout_view(request):

    logout(request)

    return redirect('home')

def about(request):
    return render(request, 'about.html')
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )
    
def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')

def contact(request):

    success = False

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:

            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            success = True

    return render(
        request,
        'contact.html',
        {
            'success': success
        }
    )
def help_center(request):
    return render(request, 'help.html')
