from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.sessions.models import Session
from .utils import *
from .forms import *

import os
from django.conf import settings
import stripe
from django.http.response import JsonResponse  # new
import json
from django.views.decorators.csrf import csrf_exempt


def account(request):
    context = {
        'orders': Order.objects.filter(user=request.user, ordered=True).order_by('ordered_date')
    }

    return render(request, 'customer-account.html', context)

@login_required
def add_to_wishlist(request, pk):
    item = Item.objects.get(pk=pk)
    # print(item)
    wish_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    messages.info(request, "Item was added to your wishlist.")
    # print(wish_item)
    return redirect('product', slug=item.slug)

@login_required
def remove_from_wishlist(request, pk):
    item = Item.objects.get(pk=pk)
    # print(item)
    wish_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    wish_item.delete()
    messages.info(request, "Item was remove from wishlist.")
    # print(wish_item)
    return redirect('view_wishlist', )


def view_wishlist(request):
    wish_items = Wishlist.objects.filter(user=request.user)
    print(wish_items)
    for item in wish_items:
        print(item.item.title)
    return render(request, 'wishlist.html', {'objects': wish_items})


def home(request):
    # print(request.content_type,'req')
    # print(request.body,'body')
    # session_key=request.session.session_key
    # s = Session.objects.get(session_key=session_key)
    # print(s['order_item'])
    # print(dir(s))
    # print(s.session_data)
    # print(session_key)
    return render(request, 'home.html')


def products(request):
    context = {
        'items': Item.objects.all().order_by('?')
    }

    return render(request, 'products.html', context)


def product(request, slug):
    item = Item.objects.get(slug=slug)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        # print(order_qs.count(),'total orders')
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                item_in_cart = True
            else:
                item_in_cart = False
        else:
            item_in_cart = False
    else:
        if item.slug in request.session.get('order_item', {}):
            item_in_cart = True
        else:
            item_in_cart = False

    context = {
        'object': item,
        'item_in_cart': item_in_cart
    }
    return render(request, 'product.html', context)


def add_to_cart(request, slug):
    if request.user.is_authenticated:
        add_to_cart_for_authenticated_user(request, slug)
        item = get_object_or_404(Item, slug=slug)
        try:
            wish_item = Wishlist.objects.get(item=item, user=request.user)
            wish_item.delete()
        except:
            pass

        return redirect("cart")
    else:
        add_to_cart_for_anonymous_user(request, slug)
        return redirect("cart")


def remove_from_cart(request, slug):
    if request.user.is_authenticated:
        print('authenticated')
        remove_from_cart_for_authenticated_user(request, slug)
        return redirect("cart")
    else:
        print('not authenticated')
        remove_from_cart_for_anonymous_user(request, slug)
        return redirect("cart")
        # return redirect('product', slug=slug)


# @login_required
def reduce_from_cart(request, slug):
    if request.user.is_authenticated:
        reduce_from_cart_for_authenticated_user(request, slug)
        return redirect("cart")

    else:
        reduce_from_cart_for_anonymous_user(request, slug)
        return redirect("cart")


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, ordered=False)
        context = {
            'object': order
        }

        return render(request, 'cart.html', context)
    else:
        order_item = request.session.get('order_item')
        print(order_item, 'order_item')
        if order_item:
            items = {}
            total_price = 0
            for slug, quantity in order_item.items():
                item = Item.objects.get(slug=slug)
                items[item] = quantity
                if item.discount_price:
                    total_price += item.discount_price
                else:
                    total_price += item.price
            context = {'object': items, 'total_price': total_price}
            return render(request, 'anonymous_cart.html', context)
        else:
            return render(request, 'anonymous_cart.html')


@login_required
def checkout(request):
    # order=Order.objects.get(user=request.user,ordered=False)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print('valid')
            shipping = form.cleaned_data.get('shipping')
            print(shipping, 'shipping')

            if shipping == 'N':  # new address
                addresses = Address.objects.filter(user=request.user, default=True)
                addresses.update(default=False)
                for address in addresses:
                    address.save()
                shipping_address = form.cleaned_data.get('shipping_address')
                phone = form.cleaned_data.get('phone')
                zip = form.cleaned_data.get('zip')
                address = Address(
                    user=request.user,
                    shipping_address=shipping_address,
                    zip=zip,
                    phone=phone,
                )
                address.default = True
                address.save()
            else:
                address = Address.objects.get(user=request.user, default=True)

            order = Order.objects.get(user=request.user, ordered=False)
            order.address = address
            order.save()

            payment_option = form.cleaned_data.get('payment_option')

            if payment_option == 'S':
                return redirect('payment', payment_option='stripe')
            elif payment_option == 'P':
                pass
            elif payment_option == 'C':
                confirm_order(order)
                return redirect('customer_account')
            else:
                pass
        else:
            print('not valid')
    else:
        order = get_object_or_404(Order, user=request.user, ordered=False)

        form = CheckoutForm()
        addresses = Address.objects.filter(user=request.user, default=True)
        # print(len(addresses))
        if addresses:
            address = addresses[0]
        else:
            address = addresses
    return render(request, 'checkout.html', {'form': form, 'address': address})


def payment(request, payment_option):
    context = {
        'public_key': settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'payment.html', context)


stripe.api_key = settings.STRIPE_SECRET_KEY

YOUR_DOMAIN = 'http://localhost:8000'


@csrf_exempt
def create_checkout_session(request):
    order = Order.objects.get(user=request.user, ordered=False)
    amount = order.get_total()
    print('amount---', amount)
    try:
        # print(request.POST,'post')
        # data = json.loads(request.POST)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency='usd',
            payment_method_types=[
                'card',

            ],
        )

        # print(intent['client_secret'])
        # print(intent,'------------------------')
        # print(intent.id,'id--------')

        # save payment info
        payment = Payment()
        payment.stripe_charge_id = intent.id
        payment.user = request.user
        payment.amount = amount
        payment.save()

        confirm_order(order, payment)

        return JsonResponse({
            'clientSecret': intent['client_secret'],
        })
    except Exception as e:
        print(e, 'e')
        return JsonResponse({'error': str(e)})


def newest_products(request):
    context = {
        'items': Item.objects.all().order_by('-created_at')
    }

    return render(request, 'products.html', context)


def low_price_products(request):
    context = {
        'items': Item.objects.all().order_by('price')
    }
    return render(request, 'products.html', context)


def high_price_products(request):
    context = {
        'items': Item.objects.all().order_by('-price')
    }
    return render(request, 'products.html', context)


def about(request):
    return render(request, 'about.html')


def contact_us(request):
    return render(request, 'contact.html')
