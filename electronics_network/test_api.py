from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from .models import NetworkNode, Product, Employee


class NetworkNodeAPITest(APITestCase):
    """Тесты для API звеньев сети"""

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

        self.employee = Employee.objects.create(
            user=self.user,
            is_active_employee=True,
            network_node=self.factory
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_network_nodes(self):
        """Тест получения списка звеньев сети"""
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_network_node(self):
        """Тест создания звена сети"""
        url = reverse('networknode-list')
        data = {
            'name': 'Розничная сеть Техно',
            'node_type': 'retail_network',
            'email': 'retail@example.com',
            'country': 'Россия',
            'city': 'Санкт-Петербург',
            'street': 'Торговая',
            'house_number': '10',
            'supplier': self.factory.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 2)

    def test_update_network_node(self):
        """Тест обновления звена сети"""
        url = reverse('networknode-detail', kwargs={'pk': self.factory.pk})
        data = {
            'name': 'Завод Электроника Обновленный',
            'node_type': 'factory',
            'email': 'factory@example.com',
            'country': 'Россия',
            'city': 'Москва',
            'street': 'Промышленная',
            'house_number': '1'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.factory.refresh_from_db()
        self.assertEqual(self.factory.name, 'Завод Электроника Обновленный')

    def test_debt_field_read_only(self):
        """Тест что поле debt_to_supplier нельзя обновлять через API"""
        url = reverse('networknode-detail', kwargs={'pk': self.factory.pk})
        data = {
            'name': 'Завод Электроника',
            'node_type': 'factory',
            'email': 'factory@example.com',
            'country': 'Россия',
            'city': 'Москва',
            'street': 'Промышленная',
            'house_number': '1',
            'debt_to_supplier': '100000.00'  # Попытка изменить задолженность
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.factory.refresh_from_db()
        # Задолженность не должна измениться
        self.assertEqual(self.factory.debt_to_supplier, Decimal('0.00'))

    def test_filter_by_country(self):
        """Тест фильтрации по стране"""
        url = reverse('networknode-by-country')
        response = self.client.get(url, {'country': 'Россия'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_clear_debt_action(self):
        """Тест действия очистки задолженности"""
        # Создаем звено с задолженностью
        retail = NetworkNode.objects.create(
            name="Розничная сеть",
            node_type="retail_network",
            email="retail@example.com",
            country="Россия",
            city="СПб",
            street="Торговая",
            house_number="10",
            supplier=self.factory,
            debt_to_supplier=Decimal('50000.00')
        )

        url = reverse('networknode-clear-debt', kwargs={'pk': retail.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retail.refresh_from_db()
        self.assertEqual(retail.debt_to_supplier, Decimal('0.00'))

    def test_hierarchy_endpoint(self):
        """Тест endpoint для получения иерархии"""
        url = reverse('networknode-hierarchy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('0', response.data)  # Уровень 0 (завод)


class ProductAPITest(APITestCase):
    """Тесты для API продуктов"""

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

        self.employee = Employee.objects.create(
            user=self.user,
            is_active_employee=True,
            network_node=self.factory
        )

        self.product = Product.objects.create(
            name="Смартфон",
            model="Galaxy S24",
            release_date=date(2024, 1, 1),
            network_node=self.factory
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_products(self):
        """Тест получения списка продуктов"""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """Тест создания продукта"""
        url = reverse('product-list')
        data = {
            'name': 'Планшет',
            'model': 'iPad Pro',
            'release_date': '2024-01-01',
            'network_node': self.factory.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
