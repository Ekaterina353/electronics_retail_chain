#!/usr/bin/env python
"""
Скрипт для создания .env файла с настройками для приложения сети электроники
"""

import os
import secrets
import string


def generate_secret_key():
    """Генерирует безопасный SECRET_KEY для Django"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))


def create_env_file():
    """Создает .env файл с настройками приложения"""

    env_content = f"""# Django настройки для сети электроники
DEBUG=1
SECRET_KEY={generate_secret_key()}
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web,db

# База данных PostgreSQL
DATABASE_URL=postgresql://postgres:postgres123@db:5432/electronics_network
POSTGRES_DB=electronics_network
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis для кэширования
REDIS_URL=redis://redis:6379/0

# Email настройки (для уведомлений)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=electronics.network@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here

# Настройки приложения
LANGUAGE_CODE=ru-ru
TIME_ZONE=Europe/Moscow

# Логирование
LOG_LEVEL=INFO

# Безопасность (для продакшена изменить)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Статические файлы
STATIC_URL=/static/
STATIC_ROOT=/app/static
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# Настройки API
API_PAGE_SIZE=20
API_MAX_PAGE_SIZE=100

# Настройки сети электроники
MAX_DEBT_AMOUNT=1000000.00
MIN_DEBT_AMOUNT=0.00
DEFAULT_CURRENCY=RUB
"""

    # Проверяем, существует ли уже .env файл
    if os.path.exists('.env'):
        print("⚠️  Файл .env уже существует!")
        response = input("Перезаписать? (y/N): ")
        if response.lower() != 'y':
            print("❌ Отменено")
            return False

    # Создаем .env файл
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан успешно!")
        print("📝 Не забудьте изменить EMAIL_HOST_PASSWORD для реальной отправки email")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании .env файла: {e}")
        return False


def main():
    """Основная функция"""
    print("🔧 Настройка .env файла для приложения сети электроники...")

    if create_env_file():
        print("\n📋 Созданные настройки:")
        print("   • База данных: PostgreSQL (electronics_network)")
        print("   • Кэширование: Redis")
        print("   • Язык: Русский")
        print("   • Часовой пояс: Europe/Moscow")
        print("   • API: Настроен для сети электроники")
        print("\n🚀 Теперь можно запустить: make install")
    else:
        print("❌ Не удалось создать .env файл")


if __name__ == '__main__':
    main()
