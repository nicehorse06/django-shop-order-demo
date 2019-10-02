from django.shortcuts import render
from .forms import OrderPostForm
from .models import Product, Order


def order(request):
    # 通过id 得到table Post的實例，如果沒有得到資料回傳404
    sent = False
    if request.method == "POST":
        # 表单被提交
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
            # sent = True
    else:
        form = OrderPostForm()
    return render(request, "order.html", {"form": form, "sent": sent})
