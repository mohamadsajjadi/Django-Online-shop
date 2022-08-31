from django import forms


class CartQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class CouponCode(forms.Form):
    code = forms.IntegerField()
