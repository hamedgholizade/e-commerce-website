from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from locations.models import Address

User = get_user_model()


class AddressAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone='9120010011', password="testpass123@"
        )
        self.other_user = User.objects.create_user(
            phone='9120010022', password="testpass123@"
        )
        self.address = Address.objects.create(
            user=self.user,
            label="Home",
            state="Tehran",
            city="Tehran",
            country="Iran",
            address_line_1="Valiasr Street",
            postal_code="1234567890"
        )
        self.url_list = reverse("locations:address-list")
        self.url_detail = reverse("locations:address-detail", kwargs={'pk': self.address.id})

    def test_create_address_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "user": self.user.id,
            "label": "Work",
            "state": "Tehran",
            "city": "Tehran",
            "country": "iran",
            "address_line_1": "Enghelab Street",
            "postal_code": "9876543210"
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 2)

    def test_create_address_unauthenticated(self):
        data = {
            "user": self.user.id,
            "label": "Home",
            "state": "Tehran",
            "city": "Tehran",
            "conutry": "iran",
            "address_line_1": "Enghelab Street",
            "postal_code": "9876543210"
        }
        response = self.client.post(self.url_list, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_addresses_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["label"], "Home")

    def test_list_addresses_not_access_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_own_address(self):
        self.client.force_authenticate(user=self.user)
        data = {"label": "Updated Home"}
        response = self.client.patch(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(self.address.label, "Updated Home")

    def test_update_other_user_address_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"label": "Hacked"}
        response = self.client.patch(self.url_detail, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_address(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.address.refresh_from_db()
        self.assertFalse(self.address.is_active)
        