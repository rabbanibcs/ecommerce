from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.sessions.models import Session
from .utils import * 
from .forms import *


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
    context={
        'items':Item.objects.all()
    }

    return render(request, 'products.html',context)


def product(request,slug):
    # print(slug,'slug')
    item=Item.objects.get(slug=slug)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        # print(order_qs.count(),'total orders')
        if order_qs.exists():
            order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            item_in_cart=True
        else:
            item_in_cart=False
    else:
        if item.slug in request.session.get('order_item',{}):
            item_in_cart=True
        else:
            item_in_cart=False
        
    context={
        'object' : item,
        'item_in_cart':item_in_cart
    }

    return render(request, 'product.html',context)

def about(request):

    return render(request, 'about.html')


def contactUs(request):

    return render(request, 'contact.html')



def add_to_cart(request, slug):
    if request.user.is_authenticated:
        add_to_cart_for_authenticated_user(request, slug)
        return redirect("cart")
    else:
        add_to_cart_for_anonymous_user(request, slug)
        return redirect("cart")


def remove_from_cart(request,slug):
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
def reduce_from_cart(request,slug):
    if request.user.is_authenticated:
        reduce_from_cart_for_authenticated_user(request, slug)
        return redirect("cart")

    else:
        reduce_from_cart_for_anonymous_user(request, slug)
        return redirect("cart")


def cart(request):

    if request.user.is_authenticated:
        order,created  = Order.objects.get_or_create(user=request.user, ordered=False)
        context = {
                    'object': order
                }
        return render(request, 'cart.html',context)
    else:
        order_item=request.session.get('order_item')
        print(order_item,'order_item')
        if order_item:
            items = {}
            for slug, quantity in order_item.items(): 
                item = Item.objects.get(slug=slug)
                items[item] = quantity
            context = {'object': items, }
            return render(request, 'anonymous_cart.html', context)
        else:
            return render(request, 'anonymous_cart.html')


def checkout(request):

    if request.method == 'POST':
        form= CheckoutForm(request.POST)
        if form.is_valid():
            # print('valid')
            shipping_address=form.cleaned_data.get('shipping_address')
            shipping_address2=form.cleaned_data.get('shipping_address2')
            zip=form.cleaned_data.get('zip')
            set_default_shipping=form.cleaned_data.get('set_default_shipping')
            use_default_shipping=form.cleaned_data.get('use_default_shipping')
            payment_option=form.cleaned_data.get('payment_option')

            address=Address(
                user=request.user,
                shipping_address=shipping_address,
                shipping_address2=shipping_address2,
                zip=zip,
                default=set_default_shipping,
            )
            address.save()
            order=Order.objects.get(user=request.user,ordered=False)
            order.address=address
            order.save()

            if payment_option=='S':
                return redirect('payment', payment_option='stripe')
            elif payment_option=='P':
                pass
            else:
                pass
        else:
            print('not valid')
    else:
        form=CheckoutForm()

    return render(request, 'checkout.html',{'form':form})


def payment(request,payment_option):
    context={
        'public_key':settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'payment.html',context)


"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from django.conf import settings
import stripe
from django.http.response import JsonResponse # new
import json
from django.views.decorators.csrf import csrf_exempt

stripe.api_key=settings.STRIPE_SECRET_KEY

YOUR_DOMAIN = 'http://localhost:8000'

@csrf_exempt
def create_checkout_session(request):
    # data = json.loads(request.body.decode("utf-8"))
    # received_json_data=json.loads(request.POST['data'])
    # print(request.POST,'post')
    # print(request.content_type,'req')
    # print(data.get('items'),'json')
    # items=data.get('items')
    # for item in items:
        # print(item['id'],'id')

    order=Order.objects.get(user=request.user,ordered=False)
    amount=order.get_total()
    print('amount---',amount)
    try:
        # print(request.POST,'post')
        # data = json.loads(request.POST)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(amount*100),
            currency='usd',
            payment_method_types=[
                'card',
                
            ],
        )

        # print(intent['client_secret'])
        # print(intent,'------------------------')
        # print(intent.id,'id--------')

        payment=Payment()
        payment.stripe_charge_id=intent.id
        payment.user=request.user
        payment.amount=amount
        payment.save()

        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        order.ordered=True
        order.payment=payment
        # order.address=address

        order.save()
        
        return JsonResponse({
            'clientSecret': intent['client_secret'],
        })
    except Exception as e:
        print(e,'e')
        return JsonResponse({'error':str(e)})
















