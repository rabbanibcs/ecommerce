from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.utils import timezone


def add_to_cart_for_authenticated_user(request, slug, quantity=1):
    # print('add_to_cart_for_authenticated_user')
    # print(quantity,'quantity')
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        # quantity=quantity
    )
    if created:
        order_item.quantity = quantity
        order_item.save()

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs.count(), 'total orders')
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += quantity
            # print(quantity,'quantity')
            order_item.save()
            messages.info(request, "This item quantity was updated.")

        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        # messages.info(request, "This item was added to your cart.")


def add_to_cart_for_anonymous_user(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = request.session.get('order_item')
    if order_item:
        quantity = order_item.get(slug)
        # print(quantity)
        if quantity:
            order_item[slug] = (1 + quantity)
            messages.info(request, "This item quantity was updated.")

        else:
            order_item[slug] = 1
            messages.info(request, "This item was added to your cart.")

    else:
        order_item = {slug: 1}
        messages.info(request, "This item was added to your cart.")

    # print(len(order_item))
    print(order_item, 'order_item')
    request.session['order_item'] = order_item


def remove_from_cart_for_authenticated_user(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from Cart.")
        else:
            messages.info(request, "This item was not in your Cart.")
    else:
        messages.info(request, "You do not have an active order")


def remove_from_cart_for_anonymous_user(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = request.session.get('order_item')
    # print((order_item),'cart before delete')

    if order_item:
        if order_item.get(slug):
            del order_item[slug]
            # print((order_item),'cart after delete')
            request.session['order_item'] = order_item
            messages.info(request, "This item was removed from Cart.")
        else:
            messages.info(request, "This item is not in Cart.")
    else:
        messages.info(request, "This item is not in Cart.")


def reduce_from_cart_for_authenticated_user(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                user=request.user,
                item=item,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "This item quantity was ruduced from Cart.")
        else:
            messages.info(request, "This item was not in your Cart.")
    else:
        messages.info(request, "You do not have an active order")


def reduce_from_cart_for_anonymous_user(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = request.session.get('order_item')
    if order_item:
        quantity = order_item.get(slug)
        # print(quantity)
        if quantity > 1:
            order_item[slug] = (quantity - 1)
            messages.info(request, "This item quantity was reduced from Cart.")

        else:
            del order_item[slug]
            messages.info(request, "This item was removed from your cart.")

    request.session['order_item'] = order_item


def confirm_order(order, payment=None):
    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    order.ordered = True
    order.ordered_date = timezone.now()
    if payment:
        order.payment = payment
    # order.address=address
    order.save()
