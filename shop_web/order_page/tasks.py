from celery import task
from django.core.mail import send_mail
from shop_web.settings import system_name, EMAIL_HOST_USER
from django.template.loader import render_to_string
from .models import Product, Order


@task
def send_email(recipient_email):
    subject = '%s館別統計資料' % system_name
    shop_id_list = Product.objects.values_list('shop_id', flat=True).distinct()
    shop_data_list = []

    for this_shop_id in shop_id_list:
        this_order_query = Order.objects.filter(product__shop_id=this_shop_id)
        # 總銷售金額
        total_sale_amount = 0
        # 總銷售數量
        total_sale_number = 0
        # 總訂單數量
        total_order_number = 0
        for this_order in this_order_query:
            total_sale_amount += this_order.qty * this_order.product.price
            total_sale_number += this_order.qty
            total_order_number += 1
        shop_data_list.append({
            'this_shop_id': this_shop_id,
            'total_sale_amount': total_sale_amount,
            'total_sale_number': total_sale_number,
            'total_order_number': total_order_number,
        })
    html_message = render_to_string(
        'shop_mail.html', {'shop_data_list': shop_data_list})
    message = 'hello user'
    mail_sent = send_mail(
        subject,
        message,
        EMAIL_HOST_USER,  # 寄件人的信箱
        [recipient_email],  # 收件人的信箱
        html_message=html_message
    )
    return mail_sent
