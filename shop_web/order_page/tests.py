from django.test import TestCase
from .models import Product, Order


class ProductTestCase(TestCase):
    def setUp(self):
        pass

    def test_order_vip_check(self):
        """確認只有VIP的客戶才能訂購VIP商品"""
        not_vip_product = Product.objects.create(
            vip=False, stock_pcs="6", price="1", shop_id='um')
        vip_product = Product.objects.create(
            vip=True, stock_pcs="6", price="1", shop_id='um')
        self.assertTrue(not_vip_product.order_vip_check(True))
        self.assertTrue(not_vip_product.order_vip_check(False))
        self.assertTrue(vip_product.order_vip_check(True))
        self.assertFalse(vip_product.order_vip_check(False))

    def test_order_qty_check(self):
        """確認庫存是否足夠出貨訂購的數量"""
        this_product = Product.objects.create(
            vip=False, stock_pcs=2, price=1, shop_id='um')
        self.assertTrue(this_product.order_qty_check('1'))
        self.assertTrue(this_product.order_qty_check('2'))
        self.assertFalse(this_product.order_qty_check('3'))


class OrderTestCase(TestCase):
    def setUp(self):
        pass

    def test_filter_is_delete(self):
        """測試Order被刪除的項不會顯示"""
        pass

    def test_top(self):
        """測試回傳數量前三大的方法"""
        pass

        def test_new_product_notice(self):
            """測試當庫存從零增加時，會有提示訊息"""
        pass

        def test_save(self):
            """確認庫存會因為Order而變化"""
        pass