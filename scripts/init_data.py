import os
import sys
import django
from django.contrib.auth.models import User
from electronics_network.models import NetworkNode, Product, Employee
from decimal import Decimal
from datetime import date

# Добавляем путь к проекту
sys.path.append('/app')

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_docker')
django.setup()


def create_superuser():
    """Создает суперпользователя"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Суперпользователь 'admin' создан (пароль: admin123)")


def create_network_hierarchy():
    """Создает иерархию сети"""
    # Завод
    factory, created = NetworkNode.objects.get_or_create(
        name="Завод Электроника",
        defaults={
            'node_type': 'factory',
            'email': 'factory@example.com',
            'country': 'Россия',
            'city': 'Москва',
            'street': 'Промышленная',
            'house_number': '1',
            'debt_to_supplier': Decimal('0.00')
        }
    )
    if created:
        print("✅ Завод создан")

    # Розничная сеть
    retail, created = NetworkNode.objects.get_or_create(
        name="Розничная сеть Техно",
        defaults={
            'node_type': 'retail_network',
            'email': 'retail@example.com',
            'country': 'Россия',
            'city': 'Санкт-Петербург',
            'street': 'Торговая',
            'house_number': '10',
            'supplier': factory,
            'debt_to_supplier': Decimal('50000.00')
        }
    )
    if created:
        print("✅ Розничная сеть создана")

    # ИП
    entrepreneur, created = NetworkNode.objects.get_or_create(
        name="ИП Смирнов",
        defaults={
            'node_type': 'individual_entrepreneur',
            'email': 'ip@example.com',
            'country': 'Россия',
            'city': 'Казань',
            'street': 'Частная',
            'house_number': '5',
            'supplier': retail,
            'debt_to_supplier': Decimal('15000.00')
        }
    )
    if created:
        print("✅ ИП создан")

    return factory, retail, entrepreneur


def create_products(factory, retail):
    """Создает продукты"""
    products_data = [
        {
            'name': 'Смартфон',
            'model': 'Galaxy S24',
            'release_date': date(2024, 1, 1),
            'network_node': factory
        },
        {
            'name': 'Планшет',
            'model': 'iPad Pro',
            'release_date': date(2024, 2, 1),
            'network_node': retail
        },
        {
            'name': 'Ноутбук',
            'model': 'MacBook Pro',
            'release_date': date(2024, 3, 1),
            'network_node': factory
        },
        {
            'name': 'Наушники',
            'model': 'AirPods Pro',
            'release_date': date(2024, 4, 1),
            'network_node': retail
        }
    ]

    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            model=product_data['model'],
            network_node=product_data['network_node'],
            defaults=product_data
        )
        if created:
            print(f"✅ Продукт '{product.name} {product.model}' создан")


def create_employees(factory, retail):
    """Создает сотрудников"""
    employees_data = [
        {
            'username': 'manager1',
            'email': 'manager1@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'network_node': factory
        },
        {
            'username': 'manager2',
            'email': 'manager2@example.com',
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'network_node': retail
        },
        {
            'username': 'employee1',
            'email': 'employee1@example.com',
            'first_name': 'Алексей',
            'last_name': 'Козлов',
            'network_node': factory
        }
    ]

    for emp_data in employees_data:
        user, created = User.objects.get_or_create(
            username=emp_data['username'],
            defaults={
                'email': emp_data['email'],
                'first_name': emp_data['first_name'],
                'last_name': emp_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Пользователь '{user.username}' создан")

        # Создаем профиль сотрудника
        employee, created = Employee.objects.get_or_create(
            user=user,
            defaults={
                'is_active_employee': True,
                'network_node': emp_data['network_node']
            }
        )
        if created:
            print(f"✅ Сотрудник '{user.username}' создан")


def main():
    """Основная функция"""
    print("🚀 Инициализация данных для сети электроники...")

    try:
        # Создаем суперпользователя
        create_superuser()

        # Создаем иерархию сети
        factory, retail, entrepreneur = create_network_hierarchy()

        # Создаем продукты
        create_products(factory, retail)

        # Создаем сотрудников
        create_employees(factory, retail)

        print("\n✅ Инициализация завершена успешно!")
        print("\n📋 Доступные учетные записи:")
        print("   Админ: admin / admin123")
        print("   Менеджер 1: manager1 / password123")
        print("   Менеджер 2: manager2 / password123")
        print("   Сотрудник: employee1 / password123")
        print("\n🌐 Доступ к приложению:")
        print("   Админ-панель: http://localhost:8000/admin/")
        print("   API: http://localhost:8000/api/")

    except Exception as e:
        print(f"❌ Ошибка при инициализации: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
