from django import template
from core.models import Order

register = template.Library()


@register.filter
def total_cart_items(user):
    qs = Order.objects.filter(user=user, ordered=False)
    if qs.exists():
        # print(qs[0].items.count(),' count')
        return qs[0].items.count()
    
    return 0



@register.filter()
def total_cart_items_(cart):
    # print(cart)
    return len(cart)

@register.filter()
def get_total_item_price(item,quantity):
    return quantity * item.price


@register.filter()
def get_total_discount_item_price(item,quantity):
    return quantity * item.discount_price

@register.filter()
def get_amount_saved(item,quantity):
    return get_total_item_price(item,quantity)-get_total_discount_item_price(item,quantity)
















