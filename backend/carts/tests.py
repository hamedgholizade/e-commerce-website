from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from carts.models import Cart, CartItem
from stores.models import Store, StoreItem
from products.models import Product


User = get_user_model()


class CartApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone="09120000001", password="Pass12345!"
        )
        self.other = User.objects.create_user(
            phone="09120000002", password="Pass12345!"
        )
        self.seller = User.objects.create_user(
            phone="09120000003", password="Pass12345!", is_seller=True
        )
        self.store = Store.objects.create(
            name="S1", description="S1-desc", seller=self.seller
        )
        self.product_1 = Product.objects.create(
            name="Widget_1", description="widget-desc", stock=999, rating=4.0
        )
        self.product_2 = Product.objects.create(
            name="Widget_2", description="widget-desc", stock=999, rating=4.0
        )
        self.product_3 = Product.objects.create(
            name="Widget_3", description="widget-desc", stock=999, rating=4.0
        )
        self.item_cheapest = StoreItem.objects.create(
            store=self.store, product=self.product_1, stock=50, price="100000", discount_price="90000"
        )
        self.item_regular = StoreItem.objects.create(
            store=self.store, product=self.product_2, stock=50, price="120000", discount_price=None
        )
        self.item_with_bad = StoreItem.objects.create(
            store=self.store, product=self.product_3, stock=50, price="BAD", discount_price=None
        )
        self.cart = Cart.objects.create(user=self.user)
        self.client.force_authenticate(self.user)

    # GET_CART
    def test_get_my_cart(self):
        url = reverse('carts:cart-detail')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)
        self.assertIn("total_price", res.data)
        self.assertIn("total_discount", res.data)
        self.assertTrue(isinstance(res.data["total_price"], str))
        self.assertTrue(isinstance(res.data["total_discount"], str))

    # ADD_ITEM
    def test_add_item_then_merge_quantity(self):
        url = reverse('carts:cart-item-list')
        res1 = self.client.post(url, {"store_item": self.item_cheapest.id, "quantity": 2}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED, res1.content)
        
        res2 = self.client.post(url, {"store_item": self.item_cheapest.id, "quantity": 3}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED, res2.content)
        self.assertEqual(
            CartItem.objects.filter(cart=self.cart, store_item=self.item_cheapest, is_active=True).count(), 1
        )
        
        ci = CartItem.objects.get(cart=self.cart, store_item=self.item_cheapest, is_active=True)
        self.assertEqual(ci.quantity, 5)

        # total = (5 * 90000 = 450000)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_price, Decimal("450000"))
        # total_discount = (100000 - 90000) * 5 = 50000
        self.assertEqual(self.cart.total_discount, Decimal("50000"))

        res_cart = self.client.get(reverse('carts:cart-detail'))
        self.assertEqual(res_cart.status_code, status.HTTP_200_OK)
        self.assertEqual(res_cart.data.get("total_price"), "450000")
        self.assertEqual(res_cart.data.get("total_discount"), "50000")
        
    def test_add_to_cart_by_url(self):
        url = reverse('carts:add-to-cart', kwargs={'pk': self.item_cheapest.id})
        res1 = self.client.post(url, format='json')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertTrue(
            CartItem.objects.filter(store_item=self.item_cheapest.id).exists()
        )
        
        res2 = self.client.post(url, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(
            CartItem.objects.get(store_item=self.item_cheapest.id).quantity, 2
        )
        
        res3 = self.client.post(url, {"quantity": 8}, format='json')
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(
            CartItem.objects.get(store_item=self.item_cheapest.id).quantity, 10
        )
        
        res4 = self.client.post(url, {"quantity": 50}, format='json')
        self.assertEqual(res4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quantity_validation_min_and_stock(self):
        url = reverse('carts:cart-item-list')

        # quantity < 1 -> 400
        res_bad = self.client.post(url, {"store_item": self.item_regular.id, "quantity": 0}, format="json")
        self.assertEqual(res_bad.status_code, status.HTTP_400_BAD_REQUEST)

        # quantity > stock -> 400
        res_over = self.client.post(url, {"store_item": self.item_regular.id, "quantity": 51}, format="json")
        self.assertEqual(res_over.status_code, status.HTTP_400_BAD_REQUEST)

        res_ok = self.client.post(url, {"store_item": self.item_regular.id, "quantity": 2}, format="json")
        self.assertEqual(res_ok.status_code, status.HTTP_201_CREATED)

    def test_soft_delete_item(self):
        res = self.client.post(
           reverse('carts:cart-item-list') , {"store_item": self.item_regular.id, "quantity": 1}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        item_id = res.data["id"]

        del_res = self.client.delete(
            reverse('carts:cart-item-detail', kwargs={'pk': item_id})
        )
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT, del_res.content)

        item = CartItem.objects.get(pk=item_id)
        self.assertFalse(item.is_active)

    def test_total_price_ignores_invalid_price_items(self):
        item_list_url = reverse('carts:cart-item-list')
        cart_url = reverse('carts:cart-detail')
        res = self.client.post(item_list_url, {"store_item": self.item_with_bad.id, "quantity": 2}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.client.post(item_list_url, {"store_item": self.item_regular.id, "quantity": 1}, format="json")
        cart_res = self.client.get(cart_url)
        self.assertEqual(cart_res.status_code, status.HTTP_200_OK)
        self.assertEqual(cart_res.data.get("total_price"), "120000")

    def test_user_cannot_access_others_cart_items(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(
            reverse('carts:cart-item-list'), {"store_item": self.item_regular.id, "quantity": 1}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        item_id = res.data["id"]

        self.client.force_authenticate(self.other)
        get_res = self.client.get(
            reverse('carts:cart-item-detail', kwargs={'pk': item_id})
        )
        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)

        patch_res = self.client.patch(
            reverse('carts:cart-item-detail', kwargs={'pk': item_id}), {"quantity": 2}, format="json"
        )
        self.assertEqual(patch_res.status_code, status.HTTP_404_NOT_FOUND)

        del_res = self.client.delete(
            reverse('carts:cart-item-detail', kwargs={'pk': item_id})
        )
        self.assertEqual(del_res.status_code, status.HTTP_404_NOT_FOUND)
        