from django.test import TestCase
from decimal import Decimal
from datetime import date
from .models import NetworkNode, Product, Employee
from django.contrib.auth.models import User


class IntegrationTest(TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем полную иерархию
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
            name="Розничная сеть Техно",
            node_type="retail_network",
            email="retail@example.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Торговая",
            house_number="10",
            supplier=self.factory,
            debt_to_supplier=Decimal('50000.00')
        )

        self.entrepreneur = NetworkNode.objects.create(
            name="ИП Смирнов",
            node_type="individual_entrepreneur",
            email="ip@example.com",
            country="Россия",
            city="Казань",
            street="Частная",
            house_number="5",
            supplier=self.retail,
            debt_to_supplier=Decimal('15000.00')
        )

        # Создаем продукты
        self.product1 = Product.objects.create(
            name="Смартфон",
            model="Galaxy S24",
            release_date=date(2024, 1, 1),
            network_node=self.factory
        )

        self.product2 = Product.objects.create(
            name="Планшет",
            model="iPad Pro",
            release_date=date(2024, 2, 1),
            network_node=self.retail
        )

        # Создаем сотрудников
        self.user1 = User.objects.create_user(
            username="employee1",
            email="emp1@example.com",
            password="testpass123"
        )

        self.user2 = User.objects.create_user(
            username="employee2",
            email="emp2@example.com",
            password="testpass123"
        )

        self.employee1 = Employee.objects.create(
            user=self.user1,
            is_active_employee=True,
            network_node=self.factory
        )

        self.employee2 = Employee.objects.create(
            user=self.user2,
            is_active_employee=True,
            network_node=self.retail
        )

    def test_complete_network_hierarchy(self):
        """Тест полной иерархии сети"""
        # Проверяем уровни
        self.assertEqual(self.factory.hierarchy_level, 0)
        self.assertEqual(self.retail.hierarchy_level, 1)
        self.assertEqual(self.entrepreneur.hierarchy_level, 2)

        # Проверяем связи
        self.assertIsNone(self.factory.supplier)
        self.assertEqual(self.retail.supplier, self.factory)
        self.assertEqual(self.entrepreneur.supplier, self.retail)

        # Проверяем обратные связи
        self.assertIn(self.retail, self.factory.clients.all())
        self.assertIn(self.entrepreneur, self.retail.clients.all())

    def test_products_distribution(self):
        """Тест распределения продуктов по сети"""
        self.assertEqual(self.factory.products.count(), 1)
        self.assertEqual(self.retail.products.count(), 1)
        self.assertEqual(self.entrepreneur.products.count(), 0)

        self.assertIn(self.product1, self.factory.products.all())
        self.assertIn(self.product2, self.retail.products.all())

    def test_debt_calculation(self):
        """Тест расчета задолженности"""
        total_debt = sum(node.debt_to_supplier for node in NetworkNode.objects.all())
        expected_debt = Decimal('65000.00')  # 50000 + 15000
        self.assertEqual(total_debt, expected_debt)

    def test_employee_network_assignment(self):
        """Тест назначения сотрудников к звеньям сети"""
        self.assertEqual(self.employee1.network_node, self.factory)
        self.assertEqual(self.employee2.network_node, self.retail)

        # Проверяем обратные связи
        self.assertIn(self.employee1, self.factory.employees.all())
        self.assertIn(self.employee2, self.retail.employees.all())

    def test_network_statistics(self):
        """Тест статистики сети"""
        # Общее количество звеньев
        total_nodes = NetworkNode.objects.count()
        self.assertEqual(total_nodes, 3)

        # Количество по типам
        factories = NetworkNode.objects.filter(node_type='factory').count()
        retail_networks = NetworkNode.objects.filter(node_type='retail_network').count()
        entrepreneurs = NetworkNode.objects.filter(node_type='individual_entrepreneur').count()

        self.assertEqual(factories, 1)
        self.assertEqual(retail_networks, 1)
        self.assertEqual(entrepreneurs, 1)

        # Общее количество продуктов
        total_products = Product.objects.count()
        self.assertEqual(total_products, 2)

        # Общее количество сотрудников
        total_employees = Employee.objects.count()
        self.assertEqual(total_employees, 2)

    def test_network_operations(self):
        """Тест операций с сетью"""
        # Добавление нового продукта
        new_product = Product.objects.create(
            name="Ноутбук",
            model="MacBook Pro",
            release_date=date(2024, 3, 1),
            network_node=self.entrepreneur
        )

        self.assertEqual(self.entrepreneur.products.count(), 1)
        self.assertIn(new_product, self.entrepreneur.products.all())

        # Изменение поставщика
        self.entrepreneur.supplier = self.factory
        self.entrepreneur.save()

        self.assertEqual(self.entrepreneur.supplier, self.factory)
        self.assertIn(self.entrepreneur, self.factory.clients.all())
        self.assertNotIn(self.entrepreneur, self.retail.clients.all())

        # Очистка задолженности
        self.retail.debt_to_supplier = Decimal('0.00')
        self.retail.save()

        self.assertEqual(self.retail.debt_to_supplier, Decimal('0.00'))
