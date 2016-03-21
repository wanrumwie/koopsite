__author__ = 'Мирослава'

import os
from django.core.management import execute_from_command_line
import django

def django_apps_setup(settings_module="koopsite.settings"):
    # Встановлення змінної оточення та ініціалізація Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    execute_from_command_line(['manage.py'])
    django.setup()

