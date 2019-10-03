from django.shortcuts import render
from django.views import View
from .forms import OrderPostForm
from .models import Product, Order


class OrderView(View):
    template_name = 'order.html'

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(OrderView, self).dispatch(*args, **kwargs)

    def get(self, request):
        form = OrderPostForm()
        product_list = Product.objects.all()
        order_list = Order.objects.all()

        return render(request, self.template_name, {"form": form, 'product_list': product_list, 'order_list': order_list})

    def post(self, request):
        form = OrderPostForm(request.POST)
        product_list = Product.objects.all()
        order_list = Order.objects.all()
        if form.is_valid():
            # 如果form中的資料皆合法則is_valid為True，cleaned_data，如果驗證失敗form.cleaned_data只會有驗證通過的數據
            cd = form.cleaned_data
            this_order = Order(
                product_id=cd['product_id'],
                qty=cd['quantity'],
                customer_id=cd['customer_id'],
            )
            this_order.save()
        return render(request, self.template_name, {"form": form, 'product_list': product_list, 'order_list': order_list})

    def delete(self, request):
        this_order_id = request.POST.get("order_id", "")
        this_delete_order = Order.objects.filter(id=this_order_id).first()
        if this_delete_order:
            this_delete_order.is_delete = True
            this_delete_order.save()

        form = OrderPostForm()
        product_list = Product.objects.all()
        order_list = Order.objects.all()

        return render(request, self.template_name, {"form": form, 'product_list': product_list, 'order_list': order_list})
