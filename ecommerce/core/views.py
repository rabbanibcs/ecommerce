from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone



def home(request):
    print(request.content_type,'req')
    print(request.body,'body')

    return render(request, 'home.html')



def products(request):
    context={
        'items':Item.objects.all()
    }

    return render(request, 'products.html',context)


def product(request,slug):
    print(slug)
    context={
        'object' : Item.objects.get(slug=slug)
    }

    return render(request, 'product.html',context)

def about(request):

    return render(request, 'about.html')
def contactUs(request):

    return render(request, 'contact.html')



# @login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs.count(),'total orders')
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart")
            
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        # return redirect("product",slug=slug)
        return redirect("cart")

# @login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from Cart.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your Cart.")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart")


# @login_required
def reduce_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            if order_item.quantity>1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "This item was ruduced from Cart.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your Cart.")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart")

def cart(request):
    order = Order.objects.get(user=request.user, ordered=False)

    context = {
                'object': order
            }

    return render(request, 'cart.html',context)


from .forms import *

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

        order.ordered=True
        order.save()
        
        return JsonResponse({
            'clientSecret': intent['client_secret'],
        })
    except Exception as e:
        print(e,'e')
        return JsonResponse({'error':str(e)})
















