from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import NetworkNode, Employee


class PermissionTest(APITestCase):
    """Тесты для прав доступа"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        self.factory = NetworkNode.objects.create(
            name="Завод Электроника",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Промышленная",
            house_number="1"
        )

        self.client = APIClient()

    def test_unauthenticated_access_denied(self):
        """Тестирование подтверждает, что неавторизованные пользователи не имеют доступа."""
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_employee_access_denied(self):
        """Тест, что неактивные сотрудники не имеют доступа"""
        Employee.objects.create(
            user=self.user,
            is_active_employee=False,  # Неактивный сотрудник
            network_node=self.factory
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_employee_profile_access_denied(self):
        """Тест, что пользователи без профиля сотрудника не имеют доступа"""
        self.client.force_authenticate(user=self.user)
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_active_employee_access_granted(self):
        """Тест, что активные сотрудники имеют доступ"""
        Employee.objects.create(
            user=self.user,
            is_active_employee=True,
            network_node=self.factory
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
