from django.test import TestCase
from .models import Product, Order

class ProductTestCase(TestCase):
    def setUp(self):
        pass

    def test_order_vip_check(self):
        """確認只有VIP的客戶才能訂購VIP商品"""
        not_vip_product = Product.objects.create(
            vip=False, stock_pcs="6", price="150", shop_id='um')
        vip_product = Product.objects.create(
            vip=True, stock_pcs="6", price="150", shop_id='um')
        self.assertTrue(not_vip_product.order_vip_check(True))
        self.assertTrue(not_vip_product.order_vip_check(False))
        self.assertTrue(vip_product.order_vip_check(True))
        self.assertFalse(vip_product.order_vip_check(False))
