from django import forms


class OrderPostForm(forms.Form):
    product_id = forms.ChoiceField(label=u'產品編號')
    quantity = forms.IntegerField(
        label='數量', widget=forms.NumberInput(attrs={'placeholder': '數量'}))
    customer_id = forms.IntegerField(
        label='顧客 ID',
        widget=forms.NumberInput(attrs={'placeholder': 'Customer ID'}))
    is_vip = forms.BooleanField(required=False, label='是否為VIP身份')

    def __init__(self, *args, **kwargs):
        super(OrderPostForm, self).__init__(*args, **kwargs)

        this_field = self.fields.get('product_id')
        if this_field:
            from .models import Product
            choices_value = [('', 'Select Product')]
            choices_value.extend(Product.objects.values_list(
                'product_id', 'product_id'))
            this_field.choices = choices_value


class ShopEmailForm(forms.Form):
    recipient_email = forms.EmailField(required=True, label=u'收件email')
