from django.test import TestCase
from .models import Product, Order
from shop_web.settings import system_name
from selenium import webdriver

# 測試的網址，可依據django起的環境更改
test_url = 'http://127.0.0.1:8000/'

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
        this_product = Product.objects.create(
            vip=False, stock_pcs=2, price=1, shop_id='um')
        this_is_delete_order = Order.objects.create(
            is_delete=True, product=this_product, qty=1, customer_id=1)

        self.assertEqual(Order.objects.count(), 0)

        this_not_delete_order = Order.objects.create(
            is_delete=False, product=this_product, qty=1, customer_id=1)

        self.assertEqual(Order.objects.count(), 1)

    def test_top(self):
        """測試回傳數量前三大的方法"""
        this_product1 = Product.objects.create(
            product_id=1, vip=False, stock_pcs=10, price=1, shop_id='um')
        this_product2 = Product.objects.create(
            product_id=2, vip=False, stock_pcs=10, price=1, shop_id='um')
        this_product3 = Product.objects.create(
            product_id=3, vip=False, stock_pcs=10, price=1, shop_id='um')
        this_product4 = Product.objects.create(
            product_id=4, vip=False, stock_pcs=10, price=1, shop_id='um')
        Order.objects.create(product_id=1, qty=5, customer_id=1)
        # this_order1_2 = Order.objects.create(
        #     product_id=1, qty=2, customer_id=2)
        # this_order1_3 = Order.objects.create(
        #     product_id=1, qty=3, customer_id=1)
        Order.objects.create(product_id=2, qty=4, customer_id=1)
        # this_order2_2 = Order.objects.create(
        #     product_id=2, qty=1, customer_id=1)
        Order.objects.create(product_id=3, qty=3, customer_id=1)
        Order.objects.create(product_id=4, qty=2, customer_id=1)

        # todo 待加上多個order一起計算的測試
        top_query = Order.objects.top()
        self.assertEqual(top_query[0], 1)
        self.assertEqual(top_query[1], 2)
        self.assertEqual(top_query[2], 3)

    def test_new_product_notice(self):
        """測試當庫存從零增加時，會有提示訊息"""
        pass

    def test_save(self):
        """確認庫存會因為Order而變化"""
        pass


class UrlRouterTestCase(TestCase):
    def setUp(self):
        pass

    def test_index_page(self):
        """測試index_page"""
        response = self.client.get('/')
        data = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn(system_name, data)
        self.assertIn('訂購系統', data)

    def test_add_order(self):
        """測試新增Order資料"""
        pass

    def test_delete_order(self):
        """測試刪除Order資料"""
        pass

# 注意Selenium測試需要下載Firefox driver
class SeleniumTestCase(TestCase):
    def setUp(self):
        # 設定開啟Firefox
        self.browser = webdriver.Firefox()
        # 結束測試關閉瀏覽器
        self.addCleanup(self.browser.quit)

    def test_index_page(self):
        # 開啟目標網址
        self.browser.get(test_url)
        self.assertIn(system_name, self.browser.title)