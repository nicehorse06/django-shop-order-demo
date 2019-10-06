import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from celery import shared_task

from .forms import OrderPostForm
from .models import Product, Order

# todo 完成decoraotr


def add_order_check(function):
    def decorator(*args, **kwargs):
        this_request = args[1]
        error_message = ''
        this_form = OrderPostForm(this_request.POST)
        if this_form.is_valid():
            cleaned_data = this_form.cleaned_data
            this_product_id = cleaned_data.get("product_id")
            this_product = Product.objects.get(product_id=this_product_id)

            is_vip = cleaned_data.get("is_vip")

            order_quantity = cleaned_data.get("quantity")
            if not this_product.order_vip_check(is_vip):
                error_message = '只有VIP身份才購買此產品'

            if not error_message and not this_product.order_qty_check(order_quantity):
                error_message = '訂購數量大於庫存量，貨源不足'

            kwargs['cleaned_data'] = cleaned_data

        print(error_message)

        kwargs['error_message'] = error_message

        return function(*args, **kwargs)

    return decorator


class OrderView(View):

    # 所有方法執行前都會做一次dispatch
    def dispatch(self, request):
        self.info_message = ''
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
            'info_message': self.info_message,
        }

        return render(request, 'order.html', context)

    @add_order_check
    def post(self, request, *args, **kwargs):
        self.error_message = kwargs.get('error_message', '')
        # 如果有錯誤訊息就不處理Order
        if not self.error_message:
            cleaned_data = kwargs.get('cleaned_data', {})
            # 創建Order
            this_order = Order(
                product_id=cleaned_data['product_id'],
                qty=cleaned_data['quantity'],
                customer_id=cleaned_data['customer_id'],
            )
            this_order.save()

            # 計算庫存
            this_product = this_order.product
            this_product.stock_pcs -= this_order.qty
            this_product.save()

        return self.get(request)

    def delete(self, request):
        this_order_id = request.POST.get("order_id", "")
        this_delete_order = Order.objects.filter(id=this_order_id).first()
        if this_delete_order:
            # 標記刪除的Order
            this_delete_order.is_delete = True
            this_delete_order.save()

            # 計算庫存
            this_product = this_delete_order.product
            if this_product.stock_pcs == 0:
                # 刪除訂單,庫存從0變回有值則提示商品到貨
                self.info_message = '有新商品(id:%d)到貨' % this_product.product_id
            this_product.stock_pcs += this_delete_order.qty
            this_product.save()

            self.order_list = Order.objects.all()
            self.product_list = Product.objects.all()

        return self.get(request)


@shared_task
def csv_export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',
                     '"Testing"', "Here's a quote"])

    return response
