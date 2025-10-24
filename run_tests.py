#!/usr/bin/env python
"""
Скрипт для запуска тестов веб-приложения сети электроники
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["electronics_network"])
    if failures:
        sys.exit(bool(failures))
