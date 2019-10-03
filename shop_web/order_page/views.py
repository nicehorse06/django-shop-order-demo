from django.shortcuts import render
from django.views import View
from .forms import OrderPostForm
from .models import Product, Order


class OrderView(View):
    template_name = 'order.html'

    def dispatch(self, *args, **kwargs):
        self.form = OrderPostForm()
        self.product_list = Product.objects.all()
        self.order_list = Order.objects.all()
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(OrderView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form, 'product_list': self.product_list, 'order_list': self.order_list})

    def post(self, request):
        this_form = OrderPostForm(request.POST)
        if this_form.is_valid():
            # 如果form中的資料皆合法則is_valid為True，cleaned_data，如果驗證失敗form.cleaned_data只會有驗證通過的數據
            cd = this_form.cleaned_data
            this_order = Order(
                product_id=cd['product_id'],
                qty=cd['quantity'],
                customer_id=cd['customer_id'],
            )
            this_order.save()
        return self.get(request)

    def delete(self, request):
        this_order_id = request.POST.get("order_id", "")
        this_delete_order = Order.objects.filter(id=this_order_id).first()
        if this_delete_order:
            this_delete_order.is_delete = True
            this_delete_order.save()
            self.order_list = Order.objects.all()

        return self.get(request)
