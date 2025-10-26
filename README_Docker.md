# Веб-приложение сети электроники - Docker

Это веб-приложение для управления сетью по продаже электроники с API-интерфейсом и админ-панелью, развернутое с помощью Docker Compose.

##  Быстрый старт

### Предварительные требования

- Docker
- Docker Compose
- Make (опционально, для удобства)

### Установка и запуск

1. **Клонируйте репозиторий и перейдите в директорию проекта**

2. **Скопируйте файл с переменными окружения:**
   ```bash
   cp env.example .env
   ```

3. **Запустите приложение одной командой:**
   ```bash
   make install
   ```
   
   Или вручную:
   ```bash
   docker-compose build
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python scripts/init_data.py
   ```

4. **Откройте в браузере:**
   - Админ-панель: http://localhost:8000/admin/
   - API: http://localhost:8000/api/

## 📋 Доступные учетные записи

После инициализации данных доступны следующие учетные записи:

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | admin | admin123 |
| Менеджер завода | manager1 | password123 |
| Менеджер розничной сети | manager2 | password123 |
| Сотрудник | employee1 | password123 |

## 🛠 Управление контейнерами

### Основные команды

```bash
# Запустить контейнеры
make up
# или
docker-compose up -d

# Остановить контейнеры
make down
# или
docker-compose down

# Показать логи
make logs
# или
docker-compose logs -f

# Подключиться к контейнеру
make shell
# или
docker-compose exec web bash
```

### Команды Django

```bash
# Выполнить миграции
make migrate
# или
docker-compose exec web python manage.py migrate

# Собрать статические файлы
make collectstatic
# или
docker-compose exec web python manage.py collectstatic --noinput

# Создать суперпользователя
make createsuperuser
# или
docker-compose exec web python manage.py createsuperuser

# Запустить тесты
make test
# или
docker-compose exec web python manage.py test
```

## 🏗 Архитектура

Приложение состоит из следующих сервисов:

- **web** - Django веб-приложение (порт 8000)
- **db** - PostgreSQL база данных (порт 5432)
- **redis** - Redis для кэширования (порт 6379)
- **nginx** - Nginx веб-сервер (порт 80)

## 📁 Структура проекта

```
.
├── Dockerfile              # Образ для Django приложения
├── docker-compose.yml      # Конфигурация Docker Compose
├── nginx.conf              # Конфигурация Nginx
├── Makefile                # Команды для управления
├── env.example             # Пример переменных окружения
├── scripts/
│   └── init_data.py        # Скрипт инициализации данных
└── config/
    └── settings_docker.py  # Настройки Django для Docker
```

## 🔧 Настройка

### Переменные окружения

Основные переменные в файле `.env`:

```env
# Django настройки
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# База данных
DATABASE_URL=postgresql://postgres:postgres123@db:5432/electronics_network

# Email (опционально)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Настройка базы данных

По умолчанию используется PostgreSQL со следующими параметрами:
- База данных: `electronics_network`
- Пользователь: `postgres`
- Пароль: `postgres123`
- Хост: `db` (внутри Docker сети)

## 🧪 Тестирование

```bash
# Запустить все тесты
make test

# Запустить конкретные тесты
docker-compose exec web python manage.py test electronics_network.test_models
docker-compose exec web python manage.py test electronics_network.test_api
```

## 📊 Мониторинг

### Проверка состояния сервисов

```bash
# Статус контейнеров
docker-compose ps

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs db
docker-compose logs nginx
```

### Health check

- Nginx: http://localhost/health/
- Django: http://localhost:8000/admin/

## 🚨 Устранение неполадок

### Проблемы с базой данных

```bash
# Пересоздать базу данных
docker-compose down -v
docker-compose up -d db
docker-compose exec web python manage.py migrate
```

### Проблемы с правами доступа

```bash
# Исправить права на файлы
sudo chown -R $USER:$USER .
```

### Очистка системы

```bash
# Полная очистка
make clean
# или
docker-compose down -v --remove-orphans
docker system prune -f
```

## 🔒 Безопасность

Для продакшена обязательно:

1. Измените `SECRET_KEY` в `.env`
2. Установите `DEBUG=False`
3. Настройте `ALLOWED_HOSTS`
4. Используйте HTTPS
5. Настройте брандмауэр
6. Регулярно обновляйте зависимости

## 📈 Масштабирование

Для увеличения производительности:

1. Добавьте больше реплик веб-сервиса
2. Настройте балансировщик нагрузки
3. Используйте внешнюю базу данных
4. Настройте Redis кластер
5. Добавьте мониторинг (Prometheus, Grafana)

## 🤝 Разработка

### Локальная разработка

```bash
# Запустить только базу данных
docker-compose up -d db redis

# Запустить Django локально
python manage.py runserver
```

### Добавление новых зависимостей

1. Добавьте в `requirements.txt`
2. Пересоберите образ: `docker-compose build`
3. Перезапустите: `docker-compose up -d`
