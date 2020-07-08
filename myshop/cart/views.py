from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from coupons.forms import CouponApllyForm
from shop.recommender import Recommender

from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=product_id
    )
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')

@require_POST
def cart_dec(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=product_id
    )
    cart.decrease(
        product=product,
        quantity = --1,
    )
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(
        Product,
        id=product_id
    )
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    product = get_object_or_404(
        Product, id=1
    )
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )
    coupon_apply_form = CouponApllyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        product = get_object_or_404(
                    Product, id=1
                    )
        cart_products = [product]
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    return render(
        request,
        'cart/detail.html',
        {
            'cart':cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products
        }
    )