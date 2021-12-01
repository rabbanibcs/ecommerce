from django.db import models
from django.shortcuts import reverse
# from django.db.models.signals import post_save
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # def get_absolute_url(self):
    #     return reverse("categories", kwargs={})

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # def get_absolute_url(self):
    #     return reverse("sub_categories", kwargs={})

    def __str__(self):
        return self.title


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_add_to_wishlist_url(self):
        return reverse("add_to_wishlist", kwargs={
            'pk': self.id
        })

    def remove_from_wishlist_url(self):
        return reverse("remove_from_wishlist", kwargs={
            'pk': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_reduce_from_cart_url(self):
        return reverse("reduce-from-cart", kwargs={
            'slug': self.slug
        })


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


# Cart...
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


# Check out...
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', related_name='address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.OneToOneField(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


ORDER_STATUS = (
    ('P', 'Processing'),
    ('S', 'Shipping'),
    ('D', 'Delivered'),
    ('R', 'Refunded'),
)
PAYMENT_STATUS = (
    ('C', 'CashOnDelivery'),
    ('P', 'Paid'),
)


class ManageOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS, max_length=1, default='P')
    payment = models.CharField(choices=PAYMENT_STATUS, max_length=1,default='P')

    def __str__(self):
        return self.order.user.email


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=11, null=True)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.shipping_address

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
