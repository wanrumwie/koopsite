#!/usr/bin/env python
import os
import sys
from koopsite.settings import SKIP_TEST

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "koopsite.settings")

    from django.core.management import execute_from_command_line

    import django.conf as conf

    # execute_from_command_line(sys.argv)
    execute_from_command_line(['manage.py','test'])
