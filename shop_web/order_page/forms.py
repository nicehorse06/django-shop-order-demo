from django import forms
from .models import Product


# todo 請美化
class OrderPostForm(forms.Form):
    product_id = forms.ChoiceField(choices=Product.objects.values_list('product_id', 'product_id'),
                                   initial='vendor_code',
                                   label=u'產品編號')
    quantity = forms.IntegerField()
    customer_id = forms.IntegerField()
    is_vip = forms.BooleanField(required=False)
