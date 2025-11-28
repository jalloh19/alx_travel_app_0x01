"""Test suite for listings endpoints."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    """Ensure the health check endpoint responds successfully."""

    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("listings-health"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})
