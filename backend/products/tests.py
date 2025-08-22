from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from products.models import Category, Product

User = get_user_model()


class CategoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone="9190010011", password="pass123@"
        )
        self.seller = User.objects.create_user(
            phone="9190010022", password="pass123@", is_seller=True
        )
    
    def test_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products:category-list')
        response = self.client.post(url, {"name": "cat-test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
        
    
    def test_seller_can_create_category(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('products:category-list')
        payload = {
            "name": "Electronics",
            "description": "All electronic devices"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertIsNone(response.data.get("parent"))

    def test_seller_can_create_category_with_parent(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('products:category-list')
        
        parent = self.client.post(url, {"name": "parent"})
        sub_parent = self.client.post(url, {"name": "sub_parent", "parent": parent.data["id"]})
        child = self.client.post(url, {"name": "child", "parent": sub_parent.data["id"]})
        self.assertEqual(parent.status_code, status.HTTP_201_CREATED, parent.content)
        self.assertEqual(sub_parent.status_code, status.HTTP_201_CREATED, sub_parent.content)
        self.assertEqual(child.status_code, status.HTTP_201_CREATED, child.content)
        
        parents = self.client.get(
            reverse('products:category-parents', kwargs={'pk': sub_parent.data['id']})
        )
        children = self.client.get(
            reverse('products:category-children', kwargs={'pk': sub_parent.data['id']})
        )
        self.assertIn(parent.data['id'], [cat['id'] for cat in parents.data])
        self.assertIn(child.data['id'], [cat['id'] for cat in children.data])


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.seller = User.objects.create_user(
            phone='9120010011', password="pass123@", is_seller=True
        )
        self.user = User.objects.create_user(
            phone='9120010022', password="pass123@", is_seller=False
        )
        self.category = Category.objects.create(name="Clothes")


    def test_list_products(self):
        product = Product.objects.create(
            name="T-Shirt", description="Red T-shirt", stock='10'
        )
        url = reverse("products:product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(product.id, [p['id'] for p in response.data["results"]])

    def test_create_product_as_seller(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse("products:product-list")
        data = {
            "name": "Shoes", "description": "Running shoes", "category": self.category.id, "stock": '5'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_normal_user_denied(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("products:product-list")
        data = {
            "name": "Shoes", "description": "Running shoes", "category": self.category.id, "stock": '5'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_by_seller(self):
        product = Product.objects.create(
            name="Hat", description="Blue hat", stock='2'
        )
        self.client.force_authenticate(user=self.seller)
        url = reverse("products:product-detail", args=[product.id])
        response = self.client.patch(url, {"description": "test-test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.description, 'test-test')

    def test_update_product_by_user_denied(self):
        product = Product.objects.create(
            name="Gloves", description="Winter gloves", stock='4'
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("products:product-detail", kwargs={'pk': product.id})
        response = self.client.patch(url, {"description": "test-test"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_seller(self):
        product = Product.objects.create(
            name="Bag", description="Travel bag", stock='1'
        )
        self.client.force_authenticate(user=self.seller)
        url = reverse("products:product-detail", kwargs={'pk': product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_as_user_denied(self):
        product = Product.objects.create(
            name="Watch", description="Smart watch", stock='2'
        )
        self.client.force_authenticate(user=self.user)
        url = reverse("products:product-detail", kwargs={'pk': product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        