# Makefile для управления Docker контейнерами

.PHONY: help build up down restart logs shell migrate collectstatic createsuperuser init-data test clean

# Показать справку
help:
	@echo "Доступные команды:"
	@echo "  build          - Собрать Docker образы"
	@echo "  up             - Запустить контейнеры"
	@echo "  down           - Остановить контейнеры"
	@echo "  restart        - Перезапустить контейнеры"
	@echo "  logs           - Показать логи"
	@echo "  shell          - Подключиться к контейнеру веб-приложения"
	@echo "  migrate        - Выполнить миграции"
	@echo "  collectstatic  - Собрать статические файлы"
	@echo "  createsuperuser - Создать суперпользователя"
	@echo "  init-data      - Инициализировать тестовые данные"
	@echo "  test           - Запустить тесты"
	@echo "  clean          - Очистить контейнеры и volumes"

# Собрать образы
build:
	docker-compose build

# Запустить контейнеры
up:
	docker-compose up -d

# Остановить контейнеры
down:
	docker-compose down

# Перезапустить контейнеры
restart:
	docker-compose restart

# Показать логи
logs:
	docker-compose logs -f

# Подключиться к контейнеру веб-приложения
shell:
	docker-compose exec web bash

# Выполнить миграции
migrate:
	docker-compose exec web python manage.py migrate

# Собрать статические файлы
collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Создать суперпользователя
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Инициализировать тестовые данные
init-data:
	docker-compose exec web python scripts/init_data.py

# Запустить тесты
test:
	docker-compose exec web python manage.py test

# Очистить контейнеры и volumes
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Создать .env файл
setup-env:
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "✅ Файл .env создан из env.example"; \
	else \
		echo "⚠️  Файл .env уже существует"; \
	fi

# Полная установка и запуск
install: setup-env build up migrate init-data
	@echo "✅ Приложение запущено!"
	@echo "🌐 Админ-панель: http://localhost:8000/admin/"
	@echo "🔗 API: http://localhost:8000/api/"

# Развертывание для продакшена
deploy: build up migrate collectstatic
	@echo "✅ Приложение развернуто для продакшена!"
