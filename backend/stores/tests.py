from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from stores.models import Store, StoreItem
from products.models import Product 

User = get_user_model()


class StorePermissionsTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.seller = User.objects.create_user(
            phone="09120000011", password="Pass12345!", is_seller=True
        )
        self.other  = User.objects.create_user(
            phone="09120000022", password="Pass12345!"
        )
        self.staff  = User.objects.create_user(
            phone="09120000033", password="Pass12345!", is_staff=True
        )
        self.superuser = User.objects.create_superuser(
            phone="09120000044", email="super@gmail.com", password="Pass12345!"
        )
        self.store = Store.objects.create(
            name="Alpha", description="Alpha Desc", seller=self.seller
        )

    # -------- Read-only access --------
    def test_anyone_can_list_and_retrieve(self):
        list_url = reverse('stores:store-list')
        res_list = self.client.get(list_url)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK, res_list.content)

        detail_url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res_detail = self.client.get(detail_url)
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK, res_detail.content)

    # -------- Create --------
    def test_seller_can_create_store_for_self(self):
        seller_test = User.objects.create_user(
            phone="09120000055", password="Pass12345!", is_seller=True
        )
        self.client.force_authenticate(seller_test)
        url = reverse('stores:store-list')
        payload = {
            "name": "SellerShopTest",
            "description": "Owned by seller",
            "seller": seller_test.id
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        self.assertEqual(res.data.get("name"), "SellerShopTest")

    def test_seller_cannot_create_store_for_other_user(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:store-list')
        payload = {
            "name": "Hijack",
            "description": "Should fail",
            "seller": self.other.id
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.content)

    def test_staff_can_create_store_for_any_seller(self):
        self.client.force_authenticate(self.staff)
        url = reverse('stores:store-list')
        payload = {
            "name": "StaffMade",
            "description": "By staff",
            "seller": self.other.id
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        self.assertEqual(res.data.get("name"), "StaffMade")

    def test_superuser_can_create_store_for_any_seller(self):
        self.client.force_authenticate(self.superuser)
        url = reverse('stores:store-list')
        payload = {
            "name": "RootMade",
            "description": "By superuser",
            "seller": self.other.id
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    # -------- Update --------
    def test_seller_can_update_own_store(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res = self.client.patch(url, {"name": "Alpha-Edited"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)

    def test_seller_cannot_transfer_ownership_on_update(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res = self.client.patch(url, {"seller": self.other.id}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.content)

    def test_other_user_cannot_update_foreign_store(self):
        self.client.force_authenticate(self.other)
        url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res = self.client.patch(url, {"name": "ShouldNot"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.content)

    def test_staff_can_update_any_store(self):
        self.client.force_authenticate(self.staff)
        url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res = self.client.patch(url, {"name": "StaffEdit"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)

    # -------- Delete (soft delete) --------
    def test_delete_is_soft_delete(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:store-detail', kwargs={"pk": self.store.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT, res.content)

        self.store.refresh_from_db()
        self.assertFalse(getattr(self.store, "is_active", True), "Store should be soft-deleted")


class StoreItemPermissionsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(
            phone="09120000066", password="Pass12345!", is_seller=True
        )
        self.other  = User.objects.create_user(
            phone="09120000077", password="Pass12345!"
        )
        self.staff  = User.objects.create_user(
            phone="09120000088", password="Pass12345!", is_staff=True
        )
        self.store = Store.objects.create(
            name="Bravo", description="B", seller=self.seller
        )
        self.product = Product.objects.create(
            name="Widget", description='test-product-description'
        )
        self.item = StoreItem.objects.create(
            store=self.store,
            product=self.product,
            stock=10,
            price="100000",         
            discount_price="90000",
        )

    # Create
    def test_seller_can_create_item_for_own_store(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:storeitem-list')
        test_product = Product.objects.create(
            name="product-test", description='test-product-description'
        )
        payload = {
            "store": self.store.id,
            "product": test_product.id,
            "stock": 5,
            "price": "120000",
            "discount_price": "110000",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    def test_seller_cannot_create_item_for_foreign_store(self):
        foreign_store = Store.objects.create(
            name="Foreign", description="x", seller=self.other
        )
        self.client.force_authenticate(self.seller)
        url = reverse('stores:storeitem-list')
        payload = {
            "store": foreign_store.id,
            "product": self.product.id,
            "stock": 2,
            "price": "1000",
            "discount_price": "900",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.content)

    def test_staff_can_create_item_any_store(self):
        self.client.force_authenticate(self.staff)
        url = reverse('stores:storeitem-list')
        test_product = Product.objects.create(
            name="product-test", description='test-product-description'
        )
        payload = {
            "store": self.store.id,
            "product": test_product.id,
            "stock": 3,
            "price": "1500",
            "discount_price": "1200",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)

    # Update
    def test_seller_can_update_item_of_own_store(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:storeitem-detail', kwargs={"pk": self.item.id})
        res = self.client.patch(url, {"stock": 99}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)

    def test_other_user_cannot_update_item(self):
        self.client.force_authenticate(self.other)
        url = reverse('stores:storeitem-detail', kwargs={"pk": self.item.id})
        res = self.client.patch(url, {"stock": 123}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.content)

    def test_staff_can_update_any_item(self):
        self.client.force_authenticate(self.staff)
        url = reverse('stores:storeitem-detail', kwargs={"pk": self.item.id})
        res = self.client.patch(url, {"stock": 77}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)

    # Delete (soft_delete)
    def test_delete_item_is_soft_delete(self):
        self.client.force_authenticate(self.seller)
        url = reverse('stores:storeitem-detail', kwargs={"pk": self.item.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT, res.content)

        self.item.refresh_from_db()
        self.assertFalse(getattr(self.item, "is_active", True), "StoreItem should be soft-deleted")
        