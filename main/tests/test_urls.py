from django.conf.urls import url
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import *  # import all from views


class TestUrls(SimpleTestCase):

    def test_menu_list(self):  # test home url
        url = reverse('main:home')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,  MenuListView)

    def test_menu_list(self):  # test home dishes
        url = reverse('main:dishes', args=['some-slug'])
        self.assertEquals(resolve(url).func,  menuDetail)

    def test_menu_list(self):  # test add to order
        url = reverse('main:add-to-order', args=['some-slug'])
        self.assertEquals(resolve(url).func,  add_to_cart)

    def test_cart(self):  # test cart
        url = reverse('main:cart')
        self.assertEquals(resolve(url).func,  get_cart_items)

    def test_delete_cart(self):  # test remove from cart
        url = reverse('main:remove-from-cart', args=[1])
        self.assertEquals(resolve(url).func.view_class,  CartDeleteView)

    def test_order_details(self):  # test order_details
        url = reverse('main:order_details')
        self.assertEquals(resolve(url).func,  order_details)

    def test_order_delivery(self):  # test order delivery
        url = reverse('main:order_delivery')
        self.assertEquals(resolve(url).func,  order_delivery)

    def test_order_delete(self):  # test order delete
        url = reverse('main:remove-from-order', args=[1])
        self.assertEquals(resolve(url).func.view_class,  OrderDeleteView)

    def test_payroll_reg(self):  # test payroll registration
        url = reverse('main:payroll_reg')
        self.assertEquals(resolve(url).func, payroll_reg)

    def test_pay_item(self):  # test payitems
        url = reverse('main:payitems')
        self.assertEquals(resolve(url).func, pay_item)

    def test_payment(self):  # test payment page
        url = reverse('main:payment-page')
        self.assertEquals(resolve(url).func, payment)

    def test_payment_details(self):  # test payment details
        url = reverse('main:payment_details')
        self.assertEquals(resolve(url).func, payment_details)

    def test_custom_meal(self):  # test custom meal
        url = reverse('main:custom_meal')
        self.assertEquals(resolve(url).func, custom_meal)

    def test_delivery_details(self):  # test custom meal
        url = reverse('main:delivery_details')
        self.assertEquals(resolve(url).func, delivery_details)

    def test_subscriptionreg(self):  # test subscription_reg
        url = reverse('main:subscription_reg', args=['some-slug'])
        self.assertEquals(resolve(url).func, subscription_reg)

    def test_delete_subscription(self):  # test remove-from-subscription
        url = reverse('main:remove-from-subscription',  args=[1])
        self.assertEquals(resolve(url).func.view_class, SubscriptionDeleteView)

    def test_breakfast(self):  # test breakfast
        url = reverse('main:breakfast')
        self.assertEquals(resolve(url).func, breakfast)

    def test_lunch(self):  # test lunch
        url = reverse('main:lunch')
        self.assertEquals(resolve(url).func, lunch)

    def test_admin_view(self):  # test lunch
        url = reverse('main:admin_view')
        self.assertEquals(resolve(url).func, admin_view)

    def test_pending_orders(self):  # test pending_orders
        url = reverse('main:pending_orders')
        self.assertEquals(resolve(url).func, pending_orders)

    def test_admin_dashboard(self):  # test admin_dashboard
        url = reverse('main:admin_dashboard')
        self.assertEquals(resolve(url).func, admin_dashboard)

    def test_update_status(self):  # test update_status
        url = reverse('main:update_status', args=[1])
        self.assertEquals(resolve(url).func, update_status)

    def test_add_reviews(self):  # test add_reviews
        url = reverse('main:add_reviews')
        self.assertEquals(resolve(url).func, add_reviews)

    def test_item_list(self):  # test item_list
        url = reverse('main:item_list')
        self.assertEquals(resolve(url).func, item_list)

    def test_add_item(self):  # test add new item
        url = reverse('main:item-create')
        self.assertEquals(resolve(url).func.view_class, ItemCreateView)

    def test_update_item(self):  # test update  item
        url = reverse('main:item-update', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, ItemUpdateView)

    def test_delete_item(self):  # test delete  item
        url = reverse('main:item-delete', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, ItemDeleteView)
