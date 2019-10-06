from django import forms
from .models import Product


class OrderPostForm(forms.Form):
    product_id = forms.ChoiceField(choices=Product.objects.values_list('product_id', 'product_id'),
                                   initial='Select Product',
                                   label=u'產品編號')
    quantity = forms.IntegerField(label='數量')
    customer_id = forms.IntegerField()
    is_vip = forms.BooleanField(required=False)
