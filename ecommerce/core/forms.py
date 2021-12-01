from django import forms
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('C', 'Cash'),
)
ADD_CHOICES = (
    ('D', 'Default'),
    ('N', 'New'),
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    zip = forms.CharField(required=False)
    shipping = forms.ChoiceField(widget=forms.RadioSelect, choices=ADD_CHOICES)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


# class CouponForm(forms.Form):
#     code = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Promo code',
#         'aria-label': 'Recipient\'s username',
#         'aria-describedby': 'basic-addon2'
#     }))


# class RefundForm(forms.Form):
#     ref_code = forms.CharField()
#     message = forms.CharField(widget=forms.Textarea(attrs={
#         'rows': 4
#     }))
#     email = forms.EmailField()


# class PaymentForm(forms.Form):
#     stripeToken = forms.CharField(required=False)
#     save = forms.BooleanField(required=False)
#     use_default = forms.BooleanField(required=False)