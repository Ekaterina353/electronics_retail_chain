from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Q
from .models import NetworkNode, Product, Employee
from .serializers import (
    NetworkNodeSerializer, NetworkNodeCreateUpdateSerializer,
    ProductSerializer, EmployeeSerializer, UserSerializer
)
from .permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с звеньями сети.
    Запрещает обновление поля 'debt_to_supplier' через API.
    """
    
    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'node_type', 'city']
    search_fields = ['name', 'email', 'city', 'country']
    ordering_fields = ['name', 'created_at', 'debt_to_supplier']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Возвращает разные сериализаторы для разных операций"""
        if self.action in ['create', 'update', 'partial_update']:
            return NetworkNodeCreateUpdateSerializer
        return NetworkNodeSerializer
    
    def get_queryset(self):
        """Возвращает queryset с оптимизацией"""
        return NetworkNode.objects.select_related('supplier').prefetch_related('products')
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Фильтрация объектов по определенной стране"""
        country = request.query_params.get('country', None)
        if country:
            queryset = self.get_queryset().filter(country__icontains=country)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Параметр country обязателен'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def clear_debt(self, request, pk=None):
        """Очистка задолженности для конкретного звена сети"""
        network_node = self.get_object()
        network_node.debt_to_supplier = 0
        network_node.save()
        serializer = self.get_serializer(network_node)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def hierarchy(self, request):
        """Получение иерархической структуры сети"""
        queryset = self.get_queryset()
        
        # Группируем по уровням иерархии
        hierarchy_data = {}
        for node in queryset:
            level = node.hierarchy_level
            if level not in hierarchy_data:
                hierarchy_data[level] = []
            
            node_data = NetworkNodeSerializer(node).data
            hierarchy_data[level].append(node_data)
        
        return Response(hierarchy_data)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с продуктами"""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['network_node', 'release_date']
    search_fields = ['name', 'model', 'network_node__name']
    ordering_fields = ['name', 'release_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Возвращает queryset с оптимизацией"""
        return Product.objects.select_related('network_node')


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра сотрудников (только чтение)"""
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active_employee', 'network_node']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['created_at', 'user__username']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Возвращает queryset с оптимизацией"""
        return Employee.objects.select_related('user', 'network_node')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра пользователей (только чтение)"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']
    
    def get_queryset(self):
        """Возвращает queryset с оптимизацией"""
        return User.objects.select_related('employee_profile__network_node')