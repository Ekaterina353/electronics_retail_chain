from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Модель звена сети по продаже электроники.
    Представляет иерархическую структуру: завод -> розничная сеть -> ИП
    """
    
    NODE_TYPES = [
        ('factory', 'Завод'),
        ('retail_network', 'Розничная сеть'),
        ('individual_entrepreneur', 'Индивидуальный предприниматель'),
    ]
    
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название звена сети'
    )
    
    node_type = models.CharField(
        max_length=30,
        choices=NODE_TYPES,
        verbose_name='Тип звена',
        help_text='Тип звена в сети'
    )
    
    # Контактная информация
    email = models.EmailField(
        verbose_name='Email',
        help_text='Электронная почта'
    )
    
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        help_text='Страна расположения'
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        help_text='Город расположения'
    )
    
    street = models.CharField(
        max_length=255,
        verbose_name='Улица',
        help_text='Название улицы'
    )
    
    house_number = models.CharField(
        max_length=20,
        verbose_name='Номер дома',
        help_text='Номер дома'
    )
    
    # Связи в сети
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        verbose_name='Поставщик',
        help_text='Поставщик оборудования'
    )
    
    # Задолженность
    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Задолженность перед поставщиком',
        help_text='Задолженность в рублях с точностью до копеек'
    )
    
    # Временные метки
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )
    
    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_node_type_display()}: {self.name}"
    
    @property
    def hierarchy_level(self):
        """
        Определяет уровень в иерархии сети.
        Завод = 0, розничная сеть = 1, ИП = 2
        """
        if self.node_type == 'factory':
            return 0
        elif self.node_type == 'retail_network':
            return 1
        elif self.node_type == 'individual_entrepreneur':
            return 2
        return -1
    
    def get_full_address(self):
        """Возвращает полный адрес"""
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"


class Product(models.Model):
    """
    Модель продукта, который продается в сети
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name='Название продукта',
        help_text='Название продукта'
    )
    
    model = models.CharField(
        max_length=255,
        verbose_name='Модель',
        help_text='Модель продукта'
    )
    
    release_date = models.DateField(
        verbose_name='Дата выхода на рынок',
        help_text='Дата выхода продукта на рынок'
    )
    
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Звено сети',
        help_text='Звено сети, которое продает этот продукт'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        unique_together = ['name', 'model', 'network_node']
    
    def __str__(self):
        return f"{self.name} {self.model}"


class Employee(models.Model):
    """
    Расширение модели пользователя для сотрудников
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Пользователь'
    )
    
    is_active_employee = models.BooleanField(
        default=True,
        verbose_name='Активный сотрудник',
        help_text='Определяет, имеет ли сотрудник доступ к API'
    )
    
    network_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Звено сети',
        help_text='Звено сети, к которому привязан сотрудник'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.network_node})"