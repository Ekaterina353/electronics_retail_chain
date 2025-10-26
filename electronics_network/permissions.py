from rest_framework import permissions
from .models import Employee


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение доступа только для активных сотрудников.
    Проверяет, что пользователь аутентифицирован и является активным сотрудником.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем, что у пользователя есть профиль сотрудника
        try:
            employee_profile = request.user.employee_profile
            return employee_profile.is_active_employee
        except Employee.DoesNotExist:
            return False
