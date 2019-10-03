from django.shortcuts import render
from django.views import View
from .forms import OrderPostForm
from .models import Product, Order


class OrderView(View):
    template_name = 'order.html'

    def get(self, request):
        form = OrderPostForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OrderPostForm(request.POST)
        if form.is_valid():
            # 如果form中的資料皆合法則is_valid為True，cleaned_data，如果驗證失敗form.cleaned_data只會有驗證通過的數據
            cd = form.cleaned_data
            this_order = Order(
                product_id=cd['product_id'],
                qty=cd['quantity'],
                customer_id=cd['customer_id'],
            )
            this_order.save()
        return render(request, self.template_name, {"form": form})
