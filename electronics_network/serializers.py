from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NetworkNode, Product, Employee


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор для звеньев сети"""
    
    hierarchy_level = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'email', 'country', 'city', 
            'street', 'house_number', 'supplier', 'supplier_name',
            'debt_to_supplier', 'hierarchy_level', 'full_address',
            'products_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['debt_to_supplier', 'created_at', 'updated_at']
    
    def get_products_count(self, obj):
        """Возвращает количество продуктов у звена сети"""
        return obj.products.count()
    
    def validate_supplier(self, value):
        """Валидация поставщика"""
        if value and value.id == self.instance.id if self.instance else False:
            raise serializers.ValidationError("Звено сети не может быть поставщиком самому себе")
        return value


class NetworkNodeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления звеньев сети (без поля debt_to_supplier)"""
    
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'email', 'country', 'city', 
            'street', 'house_number', 'supplier', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_supplier(self, value):
        """Валидация поставщика"""
        if value and value.id == self.instance.id if self.instance else False:
            raise serializers.ValidationError("Звено сети не может быть поставщиком самому себе")
        return value


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""
    
    network_node_name = serializers.CharField(source='network_node.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'model', 'release_date', 'network_node', 
            'network_node_name', 'created_at'
        ]
        read_only_fields = ['created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для сотрудников"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    network_node_name = serializers.CharField(source='network_node.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'username', 'email', 'first_name', 'last_name',
            'is_active_employee', 'network_node', 'network_node_name', 'created_at'
        ]
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    
    employee_profile = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_active', 'employee_profile'
        ]
        read_only_fields = ['id', 'is_active']
