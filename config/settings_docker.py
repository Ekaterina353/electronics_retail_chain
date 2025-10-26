import os
# from pathlib import Path


DEBUG = False

ALLOWED_HOSTS = ['*']  # Или укажите конкретные хосты

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Пример для PostgreSQL
        'NAME': os.environ.get('POSTGRES_DB', 'electronic_network'),  # Имя базы данных из переменной окружения
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),  # Пользователь базы данных
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),  # Пароль базы данных
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),  # Имя сервиса в Docker Compose
        'PORT': os.environ.get('POSTGRES_PORT', 5432),  # Порт PostgreSQL
    }
}
