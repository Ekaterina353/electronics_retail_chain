from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import NetworkNode


class AdminTest(TestCase):
    """Тесты для админ-панели"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123"
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

        self.retail = NetworkNode.objects.create(
            name="Розничная сеть",
            node_type="retail_network",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Торговая",
            house_number="10",
            supplier=self.factory,
            debt_to_supplier=Decimal('50000.00')
        )

        self.client = Client()
        self.client.login(username="admin", password="adminpass123")

    def test_admin_list_view(self):
        """Тест отображения списка в админ-панели"""
        url = reverse('admin:electronics_network_networknode_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Завод Электроника")
        self.assertContains(response, "Розничная сеть")

    def test_admin_detail_view(self):
        """Тест отображения детальной страницы в админ-панели"""
        url = reverse('admin:electronics_network_networknode_change', args=[self.factory.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Завод Электроника")

    def test_admin_filter_by_city(self):
        """Тест фильтрации по городу в админ-панели"""
        url = reverse('admin:electronics_network_networknode_changelist')
        response = self.client.get(url, {'city': 'Москва'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Завод Электроника")
        self.assertNotContains(response, "Розничная сеть")

    def test_admin_clear_debt_action(self):
        """Тест admin action для очистки задолженности"""
        url = reverse('admin:electronics_network_networknode_changelist')
        data = {
            'action': 'clear_debt',
            '_selected_action': [self.retail.pk]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        self.retail.refresh_from_db()
        self.assertEqual(self.retail.debt_to_supplier, Decimal('0.00'))
