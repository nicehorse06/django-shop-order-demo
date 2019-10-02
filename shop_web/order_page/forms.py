from django import forms
from .models import Product

# todo 這邊的選擇要改成從DB撈
test_choice = (('1', u'1'), ('2', u'2'), ('3', u'3'),)

# todo 請美化


class OrderPostForm(forms.Form):
    product_id = forms.ChoiceField(choices=test_choice,
                                   initial='vendor_code',
                                   label=u'產品編號')
    quantity = forms.IntegerField()
    customer_id = forms.IntegerField()
    is_vip = forms.BooleanField(required=False)
