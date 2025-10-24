from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet, EmployeeViewSet, UserViewSet

# Создаем роутер для API
router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet, basename='networknode')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]
