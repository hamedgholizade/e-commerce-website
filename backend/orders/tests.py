from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from carts.models import Cart, CartItem
from orders.models import Order
from locations.models import Address
from stores.models import Store, StoreItem
from products.models import Product

User = get_user_model()


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone="09120000001", password="pass1234"
        )
        self.other_user = User.objects.create_user(
            phone="09120000002", password="pass1234"
        )
        self.seller_user = User.objects.create_user(
            phone="09120000003", password="pass1234", is_seller=True
        )
        self.store = Store.objects.create(
            name="Test Store", seller=self.seller_user
        )
        self.product = Product.objects.create(
            name="Widget", description="...", stock=999, rating=4.0
        )
        self.store_item = StoreItem.objects.create(
            store=self.store, product=self.product, stock=5, price="1000", discount_price="900"
        )
        self.address = Address.objects.create(
            user=self.user,
            label="Home",
            country="Iran",
            city="Tehran",
            address_line_1="Somewhere",
            postal_code="1234567890"
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart, store_item=self.store_item, quantity=2
        )
        self.client.force_authenticate(self.user)

    # ---------- Successful checkout reduces stock ----------
    def test_successful_checkout_reduces_stock(self):
        url = reverse('orders:order-list')
        res = self.client.post(url, {"address": self.address.id}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        order_id = res.data["id"]

        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.items.count(), 1)

        self.store_item.refresh_from_db()
        self.assertEqual(self.store_item.stock, 3)

    # ---------- Atomic checkout rollback on insufficient stock ----------
    def test_checkout_rollback_on_low_stock(self):
        self.store_item.stock = 1
        self.store_item.save(update_fields=["stock"])

        url = reverse('orders:order-list')
        res = self.client.post(url, {"address": self.address.id}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, res.content)

        self.assertEqual(Order.objects.count(), 0)
        self.store_item.refresh_from_db()
        self.assertEqual(self.store_item.stock, 1)

    # ---------- Total price uses Decimal correctly ----------
    def test_total_price_decimal(self):
        url = reverse('orders:order-list')
        self.client.post(url, {"address": self.address.id}, format="json")
        order = Order.objects.first()
        self.assertEqual(Decimal(order.total_price), 1800)

    # ---------- IsOrderOwner: user cannot access others' orders ----------
    def test_user_cannot_access_others_order(self):
        order_list_url = reverse('orders:order-list')
        self.client.post(order_list_url, {"address": self.address.id}, format="json")
        order = Order.objects.first()

        self.client.force_authenticate(self.other_user)
        res = self.client.get(
            reverse('orders:order-detail', kwargs={'pk': order.id})
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- Seller sees only their store's orders ----------
    def test_seller_sees_only_their_orders(self):
        order_list_url = reverse('orders:order-list')
        seller_list_url = reverse('orders:seller-order-list')
        self.client.post(order_list_url, {"address": self.address.id}, format="json")
        order = Order.objects.first()

        another_seller = User.objects.create_user(
            phone="09120000004", password="pass1234", is_seller=True
        )
        self.client.force_authenticate(another_seller)
        res = self.client.get(seller_list_url)
        self.assertEqual(len(res.data), 0)

        self.client.force_authenticate(self.seller_user)
        res2 = self.client.get(seller_list_url)
        self.assertTrue(any(o["id"] == order.id for o in res2.data))

    # ---------- Seller can update only their own order status ----------
    def test_seller_can_update_only_own_order_status(self):
        order_list_url = reverse('orders:order-list')
        self.client.post(order_list_url, {"address": self.address.id}, format="json")
        order = Order.objects.first()

        # Another seller tries to update -> forbidden or not found
        another_seller = User.objects.create_user(
            phone="09120000005", password="pass1234", is_seller=True
        )
        self.client.force_authenticate(another_seller)
        res = self.client.patch(
            reverse('orders:seller-order-detail', kwargs={'pk': order.id}),
            {"status": Order.ORDER_DELIVERED},
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Correct seller updates -> allowed
        self.client.force_authenticate(self.seller_user)
        res2 = self.client.patch(
            reverse('orders:seller-order-detail', kwargs={'pk': order.id}),
            {"status": Order.ORDER_DELIVERED},
            format="json"
        )
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.ORDER_DELIVERED)
