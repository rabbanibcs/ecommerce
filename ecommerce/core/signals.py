# from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from .models import *
import json
from allauth.account.signals import user_logged_in
from django.dispatch.dispatcher import receiver
from .utils import add_to_cart_for_authenticated_user


@receiver(user_logged_in)
def add_to_cart(sender, request, user, **kwargs):
    order_item = request.session.get('order_item')
    if order_item:
        for item, quantity in order_item.items():
            # print(item)
            # print(quantity)
            add_to_cart_for_authenticated_user(request, item, quantity)


@receiver(post_save, sender=Order)
def order_status(sender, instance, created, **kwargs):
    if instance.ordered:
        confirm_order = ManageOrder()
        confirm_order.order_id = instance.id
        confirm_order.status = 'P'
        if instance.payment:
            confirm_order.payment = 'P'
        else:
            confirm_order.payment = 'C'
        confirm_order.save()
