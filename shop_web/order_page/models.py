from django.db import models
from django.db.models import Sum


class Product(models.Model):
    product_id = models.AutoField(primary_key=True, verbose_name=u'商品id')
    stock_pcs = models.PositiveIntegerField(verbose_name=u'商品庫存數量')
    price = models.PositiveIntegerField(verbose_name=u'商品單價')
    shop_id = models.CharField(max_length=5, verbose_name=u'商品所屬館別')
    vip = models.BooleanField(
        default=True, verbose_name=u'是否為VIP', help_text=u'True => VIP限定/ False =>無限制購買對象')

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'商品id(%d)館別(%s)' % (self.product_id, self.shop_id)

    def order_vip_check(self, order_vip):
        if self.vip:
            if not order_vip:
                # 商品為VIP，但order非VIP身份時驗失敗
                return False
        return True

    def order_qty_check(self, order_qty):
        if self.stock_pcs < int(order_qty):
            # 數量不足
            return False
        return True


class OrdersManager(models.Manager):
    def get_queryset(self):
        # 隱藏刪除的項
        return super().get_queryset().filter(is_delete=False)

    def top(self, top_num=3):
        # 回傳前3大的訂購數量的product number
        return self.values('product_id').annotate(Sum('qty')).order_by('-qty__sum').values_list('product_id', flat=True)[:top_num]


class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'訂單id')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=u'商品')
    qty = models.PositiveIntegerField(verbose_name=u'購買數量')
    customer_id = models.PositiveIntegerField(verbose_name=u'Customer ID')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否刪除')

    objects = OrdersManager()

    class Meta:
        verbose_name = u'訂單'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'訂單id(%s)' % self.id

    def price(self):
        return self.product.price
    price.short_description = u'商品單價'

    def shop_id(self):
        return self.product.shop_id
    shop_id.short_description = u'商品所屬館別'

    def new_product_notice(self):
        info_message = ''
        if self.product.stock_pcs == 0:
            # 刪除訂單,庫存從0變回有值則提示商品到貨
            info_message = '，有新商品(id:%d)到貨' % self.product.product_id
        return info_message

    def save(self, *args, **kwargs):
        this_product = self.product
        # Order的更新要計算產品庫存
        if self.is_delete == True:
            this_product.stock_pcs += self.qty
        else:
            this_product.stock_pcs -= self.qty
        this_product.save()
        super(Order, self).save(*args, **kwargs)
