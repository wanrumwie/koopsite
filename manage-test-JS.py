#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koopsite.settings")

    from django.core.management import execute_from_command_line

    # execute_from_command_line(sys.argv)
    execute_from_command_line(['manage.py','test', 'js_tests'])
