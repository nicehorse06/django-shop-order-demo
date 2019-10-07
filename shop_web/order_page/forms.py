from django import forms


class OrderPostForm(forms.Form):
    product_id = forms.ChoiceField(initial='Select Product',
                                   label=u'產品編號')
    quantity = forms.IntegerField(label='數量')
    customer_id = forms.IntegerField()
    is_vip = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super(OrderPostForm, self).__init__(*args, **kwargs)

        this_field = self.fields.get('product_id')
        if this_field:
            from .models import Product
            this_field.choices = Product.objects.values_list('product_id', 'product_id')
