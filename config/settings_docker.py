import os
from pathlib import Path
from .settings import *

# Переопределяем настройки для Docker окружения

# Дополнительные хосты для Docker
ALLOWED_HOSTS.extend(['web', 'db', 'nginx'])

# Переопределяем пути для Docker
STATIC_ROOT = '/app/static'
MEDIA_ROOT = '/app/media'

# Логирование в Docker (только в консоль)
LOGGING['handlers'] = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
    },
}
LOGGING['root']['handlers'] = ['console']
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['electronics_network']['handlers'] = ['console']
