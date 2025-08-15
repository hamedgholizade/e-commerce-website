from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone = "9120000001"
        self.email = "user1@example.com"
        self.password = "TestPass123!"
        self.user = User.objects.create_user(
            phone=self.phone,
            email=self.email,
            password=self.password,
            first_name="Ali",
            last_name="Rezai",
        )

    # ---------- Register ----------
    def test_register_success_and_password_not_leaked(self):
        url = reverse('accounts:register')
        payload = {
            "phone": "09120620002",
            "email": "user2@example.com",
            "password": "AnotherPass123!",
            "first_name": "Sara",
            "last_name": "Ahmadi",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.content)
        self.assertNotIn("password", res.data, "Password must be write_only and not in response")
        self.assertTrue(User.objects.filter(phone="9120620002").exists())
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_register_duplicate_phone_returns_400(self):
        url = reverse('accounts:register')
        payload = {
            "phone": self.phone,
            "email": "dup@example.com",
            "password": "NewPass123!",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Login (password) ----------
    def test_login_with_phone_and_password(self):
        url = reverse('accounts:login-token')
        payload = {
            "email_or_phone": self.phone,
            "password": self.password
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.content)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_with_email_and_password_via_backend(self):
        url = reverse('accounts:login-token')
        payload = {
            "email_or_phone": self.email,
            "password": self.password,
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)

    def test_login_invalid_credentials(self):
        url = reverse('accounts:login-token')
        payload = {"email_or_phone": self.phone, "password": "WrongPass!"}
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Profile update & password hashing ----------
    def test_profile_update_hashes_password(self):
        login_url = reverse('accounts:login-token')
        login_res = self.client.post(
            login_url, {"email_or_phone": self.phone, "password": self.password}, format="json"
        )
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        profile_url = reverse('accounts:profile')
        new_password = "BrandNewPass456!"
        res = self.client.patch(profile_url, {"password": new_password}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    # ---------- OTP ----------
    def test_otp_request_and_login_success(self):
        cache.clear()
        url = reverse('accounts:login-otp')

        send_res = self.client.post(url, {"email_or_phone": self.phone}, format="json")
        self.assertEqual(send_res.status_code, status.HTTP_202_ACCEPTED)

        cached_code = cache.get(f"otp-sent:phone:{self.phone}")
        self.assertIsNotNone(cached_code, "OTP code must be stored in cache")

        login_res = self.client.post(
            url,
            {"email_or_phone": self.phone, "otp_code": str(cached_code)},
            format="json",
        )
        self.assertEqual(login_res.status_code, status.HTTP_200_OK, login_res.content)
        self.assertIn("access", login_res.data)
        self.assertIn("refresh", login_res.data)

    def test_otp_wrong_code_limited_attempts(self):
        cache.clear()
        url = reverse('accounts:login-otp')
        self.client.post(url, {"email_or_phone": self.phone}, format="json")
        last_status = None
        for _ in range(6):
            res = self.client.post(
                url,
                {"email_or_phone": self.phone, "otp_code": "00000"},
                format="json",
            )
            last_status = res.status_code
        self.assertIn(last_status, (429, status.HTTP_429_TOO_MANY_REQUESTS))

    def test_otp_request_rate_limit(self):
        cache.clear()
        url = reverse('accounts:login-otp')
        first = self.client.post(url, {"email_or_phone": self.phone}, format="json")
        self.assertEqual(first.status_code, status.HTTP_202_ACCEPTED)

        second = self.client.post(url, {"email_or_phone": self.phone}, format="json")
        self.assertIn(second.status_code, (429, status.HTTP_429_TOO_MANY_REQUESTS))
