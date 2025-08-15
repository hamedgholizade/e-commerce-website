from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from products.models import Product
from stores.models import Store
from reviews.models import Review

User = get_user_model()


class ReviewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.user = User.objects.create_user(
            phone="09120000001", password="pass1234"
        )
        self.other_user = User.objects.create_user(
            phone="09120000002", password="pass1234"
        )
        self.admin_user = User.objects.create_superuser(
            phone="09120000003", password="adminpass"
        )
        self.product = Product.objects.create(
            name="Widget", description="widget-desc", stock=10, rating=4.0
        )
        self.store = Store.objects.create(
            name="Test Store", seller=self.user
        )
        self.client.force_authenticate(self.user)

    # ---------- Create review for product ----------
    def test_create_review_for_product(self):
        payload = {"product": self.product.id, "comment": "Great!"}
        res = self.client.post(reverse('reviews:review-list'), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        review = Review.objects.get(id=res.data["id"])
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)

    # ---------- Create review for store ----------
    def test_create_review_for_store(self):
        payload = {"store": self.store.id, "comment": "Nice store!"}
        res = self.client.post(reverse('reviews:review-list'), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(id=res.data["id"])
        self.assertEqual(review.store, self.store)

    # ---------- Prevent duplicate review for same product ----------
    def test_prevent_duplicate_review_product(self):
        Review.objects.create(user=self.user, product=self.product, comment="One")
        payload = {"product": self.product.id, "comment": "Two", "rating": 3}
        res = self.client.post(reverse('reviews:review-list'), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Prevent duplicate review for same store ----------
    def test_prevent_duplicate_review_store(self):
        Review.objects.create(user=self.user, store=self.store, comment="Old")
        payload = {"store": self.store.id, "comment": "New", "rating": 5}
        res = self.client.post(reverse('reviews:review-list'), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Owner can update their review ----------
    def test_owner_can_update(self):
        review = Review.objects.create(user=self.user, product=self.product, comment="Old")
        url = reverse('reviews:review-detail', kwargs={'pk': review.id})
        res = self.client.patch(url, {"comment": "Updated"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.comment, "Updated")

    # ---------- Non-owner cannot update ----------
    def test_non_owner_cannot_update(self):
        review = Review.objects.create(user=self.user, product=self.product, comment="Old")
        url = reverse('reviews:review-detail', kwargs={'pk': review.id})
        self.client.force_authenticate(self.other_user)
        res = self.client.patch(url, {"comment": "Hack"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Admin can update any review ----------
    def test_admin_can_update(self):
        review = Review.objects.create(user=self.user, product=self.product, comment="Old")
        url = reverse('reviews:review-detail', kwargs={'pk': review.id})
        self.client.force_authenticate(self.admin_user)
        res = self.client.patch(url, {"comment": "Admin edit"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.comment, "Admin edit")

    # ---------- Owner can delete ----------
    def test_owner_can_delete(self):
        review = Review.objects.create(user=self.user, product=self.product, comment="Del")
        url = reverse('reviews:review-detail', kwargs={'pk': review.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=review.id, is_active=True).exists())

    # ---------- Non-owner cannot delete ----------
    def test_non_owner_cannot_delete(self):
        review = Review.objects.create(user=self.user, product=self.product, comment="Del")
        url = reverse('reviews:review-detail', kwargs={'pk': review.id})
        self.client.force_authenticate(self.other_user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- Filter by parent__isnull ----------
    def test_filter_parent_isnull(self):
        parent_review = Review.objects.create(
            user=self.user, product=self.product, comment="Parent"
        )
        child_review = Review.objects.create(
            user=self.user, product=self.product, comment="Child", parent=parent_review
        )
        res_only_parents = self.client.get(reverse('reviews:review-list'), {"parent__isnull": "true"})
        self.assertTrue(all(r["parent"] is None for r in res_only_parents.data))
        