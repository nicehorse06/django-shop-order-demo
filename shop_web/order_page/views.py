import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from celery import shared_task
from django.db.models import Sum

from shop_web.settings import system_name
from .forms import OrderPostForm
from .models import Product, Order

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
            'system_name': system_name
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

            self.info_message = '添加訂單成功'

        return self.get(request)

    def delete(self, request):
        this_order_id = request.POST.get("order_id", "")
        this_delete_order = Order.objects.filter(id=this_order_id).first()
        if this_delete_order:
            self.info_message = '添加訂單取消成功'
            self.info_message += this_delete_order.new_product_notice()

            # 標記刪除的Order
            this_delete_order.is_delete = True
            this_delete_order.save()

            self.order_list = Order.objects.all()
            self.product_list = Product.objects.all()

        return self.get(request)


@shared_task
def csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['館別', '總銷售金額', '總銷售數量', '總訂單數量'])
    shop_id_list = Product.objects.values_list('shop_id', flat=True).distinct()
    for this_shop_id in shop_id_list:
        this_order_query = Order.objects.filter(product__shop_id=this_shop_id)
        total_sale_amount = 0
        total_sale_number = 0
        total_order_number = 0
        for this_order in this_order_query:
            total_sale_amount += this_order.qty * this_order.product.price
            total_sale_number += this_order.qty
            total_order_number += 1

        writer.writerow([this_shop_id, total_sale_amount,
                         total_sale_number, total_order_number])

    return response
