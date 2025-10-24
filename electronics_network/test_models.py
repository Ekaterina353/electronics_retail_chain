from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from .models import NetworkNode, Product, Employee


class NetworkNodeModelTest(TestCase):
    """Тесты для модели NetworkNode"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.factory = NetworkNode.objects.create(
            name="Завод Электроника",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Промышленная",
            house_number="1",
            debt_to_supplier=Decimal('0.00')
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
            city="Рязань",
            street="Частная",
            house_number="5",
            supplier=self.retail,
            debt_to_supplier=Decimal('15000.00')
        )
    
    def test_network_node_creation(self):
        """Тест создания звена сети"""
        self.assertEqual(self.factory.name, "Завод Электроника")
        self.assertEqual(self.factory.node_type, "factory")
        self.assertEqual(self.factory.debt_to_supplier, Decimal('0.00'))
    
    def test_hierarchy_level(self):
        """Тест определения уровня иерархии"""
        self.assertEqual(self.factory.hierarchy_level, 0)
        self.assertEqual(self.retail.hierarchy_level, 1)
        self.assertEqual(self.entrepreneur.hierarchy_level, 2)
    
    def test_full_address(self):
        """Тест формирования полного адреса"""
        expected_address = "Россия, Москва, Промышленная, 1"
        self.assertEqual(self.factory.get_full_address(), expected_address)
    
    def test_supplier_relationship(self):
        """Тест связи с поставщиком"""
        self.assertIsNone(self.factory.supplier)
        self.assertEqual(self.retail.supplier, self.factory)
        self.assertEqual(self.entrepreneur.supplier, self.retail)
    
    def test_clients_relationship(self):
        """Тест обратной связи с клиентами"""
        self.assertIn(self.retail, self.factory.clients.all())
        self.assertIn(self.entrepreneur, self.retail.clients.all())
    
    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.factory), "Завод: Завод Электроника")
        self.assertEqual(str(self.retail), "Розничная сеть: Розничная сеть Техно")


class ProductModelTest(TestCase):
    """Тесты для модели Product"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.factory = NetworkNode.objects.create(
            name="Завод Электроника",
            node_type="factory",
            email="factory@example.com",
            country="Россия",
            city="Москва",
            street="Промышленная",
            house_number="1"
        )
        
        self.product = Product.objects.create(
            name="Смартфон",
            model="Galaxy S24",
            release_date=date(2024, 1, 1),
            network_node=self.factory
        )
    
    def test_product_creation(self):
        """Тест создания продукта"""
        self.assertEqual(self.product.name, "Смартфон")
        self.assertEqual(self.product.model, "Galaxy S24")
        self.assertEqual(self.product.network_node, self.factory)
    
    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.product), "Смартфон Galaxy S24")
    
    def test_unique_together_constraint(self):
        """Тест уникальности комбинации name, model, network_node"""
        # Попытка создать дубликат должна вызвать ошибку
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Смартфон",
                model="Galaxy S24",
                release_date=date(2024, 1, 1),
                network_node=self.factory
            )


class EmployeeModelTest(TestCase):
    """Тесты для модели Employee"""
    
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
    
    def test_employee_creation(self):
        """Тест создания сотрудника"""
        self.assertEqual(self.employee.user, self.user)
        self.assertTrue(self.employee.is_active_employee)
        self.assertEqual(self.employee.network_node, self.factory)
    
    def test_string_representation(self):
        """Тест строкового представления"""
        expected = f"{self.user.get_full_name() or self.user.username} ({self.factory})"
        self.assertEqual(str(self.employee), expected)
