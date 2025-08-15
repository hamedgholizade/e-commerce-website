from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from locations.models import Address
from orders.models import Order
from payments.models import Payment

User = get_user_model()


class PaymentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            phone="09120000001", password="pass1234"
        )
        self.user2 = User.objects.create_user(
            phone="09120000002", password="pass1234"
        )
        self.address1 = Address.objects.create(
            user=self.user1,
            label="Home-user1",
            country="Iran",
            city="Tehran",
            address_line_1="Somewhere",
            postal_code="1234567890"
        )
        self.address2 = Address.objects.create(
            user=self.user2,
            label="Home-user2",
            country="Iran",
            city="Tehran",
            address_line_1="Somewhere",
            postal_code="1239087654"
        )
        self.order1 = Order.objects.create(
            customer=self.user1, address=self.address1, total_price='1000'
        )
        self.order2 = Order.objects.create(
            customer=self.user2, address=self.address2, total_price='2000'
        )
        self.payment1 = Payment.objects.create(
            order=self.order1, amount=1000, status=2, transaction_id='132465987000654'
        )
        self.payment2 = Payment.objects.create(
            order=self.order2, amount=2000, status=1, transaction_id='465498701331689'
        )

    def test_login_required_for_list(self):
        """Anonymous users should get 401 for payments list"""
        res = self.client.get(reverse('payments:payment-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_payments(self):
        """User1 should only see their own payment"""
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('payments:payment-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], self.payment1.id)

    def test_read_only_endpoints(self):
        """POST, PUT, PATCH, DELETE should not be allowed"""
        self.client.force_authenticate(self.user1)

        # POST
        res = self.client.post(reverse('payments:payment-list'), {"order": self.order1.id, "amount": 500})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # PUT/PATCH
        res = self.client.put(reverse('payments:payment-list'), {"status": 2})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.patch(reverse('payments:payment-list'), {"status": 2})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        res = self.client.delete(reverse('payments:payment-list'))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
