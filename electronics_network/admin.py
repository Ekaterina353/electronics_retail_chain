from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import NetworkNode, Product, Employee


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'node_type', 'email', 'city', 'country',
        'supplier_link', 'debt_to_supplier', 'hierarchy_level', 'created_at'
    ]
    list_filter = [
        'node_type', 'country', 'city', 'created_at'
    ]
    search_fields = [
        'name', 'email', 'city', 'country', 'street'
    ]
    readonly_fields = ['created_at', 'updated_at', 'hierarchy_level']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'node_type', 'email')
        }),
        ('Адрес', {
            'fields': ('country', 'city', 'street', 'house_number')
        }),
        ('Связи в сети', {
            'fields': ('supplier', 'debt_to_supplier')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'hierarchy_level'),
            'classes': ('collapse',)
        }),
    )

    actions = ['clear_debt']

    def supplier_link(self, obj):
        """Создает ссылку на поставщика"""
        if obj.supplier:
            url = reverse('admin:electronics_network_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Поставщик'
    supplier_link.admin_order_field = 'supplier__name'

    def hierarchy_level(self, obj):
        """Показывает уровень в иерархии"""
        level = obj.hierarchy_level
        if level == 0:
            return format_html('<span style="color: green; font-weight: bold;">Завод (0)</span>')
        elif level == 1:
            return format_html('<span style="color: blue; font-weight: bold;">Розничная сеть (1)</span>')
        elif level == 2:
            return format_html('<span style="color: orange; font-weight: bold;">ИП (2)</span>')
        return f'Уровень {level}'

    hierarchy_level.short_description = 'Уровень иерархии'

    def clear_debt(self, request, queryset):
        """Admin action для очистки задолженности"""
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(
            request,
            f'Задолженность очищена для {updated} объектов.'
        )

    clear_debt.short_description = 'Очистить задолженность перед поставщиком'

    def get_queryset(self, request):
        """Оптимизирует запросы"""
        return super().get_queryset(request).select_related('supplier')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'model', 'release_date', 'network_node', 'created_at'
    ]
    list_filter = [
        'release_date', 'network_node__node_type', 'network_node__country', 'created_at'
    ]
    search_fields = [
        'name', 'model', 'network_node__name'
    ]
    readonly_fields = ['created_at']

    fieldsets = (
        ('Информация о продукте', {
            'fields': ('name', 'model', 'release_date')
        }),
        ('Связи', {
            'fields': ('network_node',)
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Оптимизирует запросы"""
        return super().get_queryset(request).select_related('network_node')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'is_active_employee', 'network_node', 'created_at'
    ]
    list_filter = [
        'is_active_employee', 'network_node__node_type', 'created_at'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'user__email'
    ]
    readonly_fields = ['created_at']

    fieldsets = (
        ('Информация о сотруднике', {
            'fields': ('user', 'is_active_employee', 'network_node')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Оптимизирует запросы"""
        return super().get_queryset(request).select_related('user', 'network_node')


# Настройка заголовков админ-панели
admin.site.site_header = 'Админ-панель сети электроники'
admin.site.site_title = 'Сеть электроники'
admin.site.index_title = 'Управление сетью электроники'
