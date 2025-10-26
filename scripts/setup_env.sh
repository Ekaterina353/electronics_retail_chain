#!/bin/bash

# Скрипт для создания .env файла

if [ ! -f .env ]; then
    echo "Создание .env файла..."
    cp env.example .env
    echo "✅ Файл .env создан из env.example"
    echo "📝 Не забудьте изменить SECRET_KEY для продакшена!"
else
    echo "⚠️  Файл .env уже существует"
fi
