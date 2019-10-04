from django.shortcuts import render
from django.views import View
from .forms import OrderPostForm
from .models import Product, Order

# todo 完成decoraotr


def add_order_check(function):
    def decorator(*args, **kwargs):
        this_request = args[1]
        error_message = ''
        this_product_id = this_request.POST.get("product_id")
        this_product = Product.objects.get(product_id=this_product_id)

        this_quantity = this_request.POST.get("quantity", False)

        is_vip = this_request.POST.get("is_vip", False)

        order_quantity = this_request.POST.get("quantity", 0)
        if not this_product.order_vip_check(is_vip):
            error_message = '只有VIP身份才購買此產品'

        if not error_message and not this_product.order_qty_check(order_quantity):
            error_message = '訂購數量不能大於庫存量'

        print(error_message)

        kwargs['error_message'] = error_message

        return function(*args, **kwargs)

    return decorator


class OrderView(View):

    # 所有方法執行前都會做一次dispatch
    def dispatch(self, request):
        self.error_message = ''
        self.form = OrderPostForm()
        self.product_list = Product.objects.all()
        self.order_list = Order.objects.all()
        self.top_sell_id_list = Order.objects.top()
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(request)
        return super(OrderView, self).dispatch(request)

    def get(self, request):
        context = {
            'form': self.form,
            'product_list': self.product_list,
            'order_list': self.order_list,
            'top_sell_id_list': self.top_sell_id_list,
            'error_message': self.error_message,
        }

        return render(request, 'order.html', context)

    @add_order_check
    def post(self, request, *args, **kwargs):
        self.error_message = kwargs.get('error_message', '')
        if not self.error_message:
            this_form = OrderPostForm(request.POST)
            if this_form.is_valid():
                # 如果form中的資料皆合法則is_valid為True，cleaned_data，如果驗證失敗form.cleaned_data只會有驗證通過的數據
                cd = this_form.cleaned_data

                this_order = Order(
                    product_id=cd['product_id'],
                    qty=cd['quantity'],
                    customer_id=cd['customer_id'],
                )

                # # todo 這段要加到decarator
                # this_product = this_order.product

                # # 重新計算庫存
                # this_product.stock_pcs = this_product.stock_pcs - this_order.qty
                # this_product.save()

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
