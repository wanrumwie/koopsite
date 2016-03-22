"""
Django settings for koopsite project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wzl%b&lwgnl1ng71(5%ru7tq5xx-x*@2qc+7&h4#y1&o(ptpns'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# Needed when DEBUG=False
ALLOWED_HOSTS = ['wanrumwie.pythonanywhere.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'koopsite',         # "кореневий" каталог koopsite.koopsite
                        # теж оголошується аплікацією, дозволяє робити
                        # міграції моделей, описаних в koopsite.models.py
    'flats',
    'folders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'koopsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'js_tests/templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'koopsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('uk', _('Ukrainian')),
)

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Абсолютний шлях до каталога, в який collectstatic збере статичні файли
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
# URL, що вказує на каталог STATIC_ROOT
STATIC_URL = '/static/'

# Абсолютний шлях до каталога, де зберігаються "медіа"-файли
# URL, який вказує на каталог MEDIA_ROOT, викор. для роботи з файлами.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

# Список каталогів, де collectstatic та тег шаблону {% static %} будуть шукати статичні файли
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "js_tests"), # для посилання на js-тести
    # os.path.join(BASE_DIR, "static/koopsite"),
    # os.path.join(BASE_DIR, "static/folders"),
    # os.path.join(BASE_DIR, "static/flats"),
    # os.path.join(BASE_DIR, "static/lists"), # вміст теки перенесено до lists/static
    MEDIA_ROOT,
)

# На цей url будуть скеровуватися незалоговані користувачі
# при спробі доступу до view, задекорованих @login_required

LOGIN_URL = '/noaccess/'

# Settings for using GMail as my SMTP server for django

# TODO-2016 01 20 купити акаунт на pythonanywhere.com оскільки "you cannot use SMTP on Free accounts"
# https://help.pythonanywhere.com/pages/SMTPForFreeUsers - нахабно стверджують, що вони зробили виняток для gmail.com
# але мені вдалось "пропхати" пошту лише раз, решта були заблоковані gmail'ом.
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'adm.koopsite@gmail.com'
EMAIL_HOST_PASSWORD = 'Gfcsxybq2000'

# Поштовий сервер для сайту на pythonanywhere
# python_any_where = True
python_any_where = False
if python_any_where:
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = "wanrumwie@gmail.com"
    EMAIL_HOST_PASSWORD = 'Protas'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


# ---------------------------------------------------------------
# Власні глобальні параметри:

# Адреса сайту, яка буде вказуватися в електронних листах:
SITE_ADDRESS = "wanrumwie.pythonanywhere.com"

# Максимальний розмір файла, який дозволяється завантажувати на сервер:
# MAX_FILE_SIZE = 20000000
MAX_FILE_SIZE = 200000000

# Максимальний розмір zip-файла, який дозволяється завантажувати з сервера:
MAX_ZIP_FILE_SIZE = 20000000

# id сайтів в списку admin
# 1 = production, 2 = localhost (на даний момент)
if DEBUG:
    SITE_ID = 2
else:
    SITE_ID = 1

# ABSOLUTE_URL_OVERRIDES = {
#     'auth.user': lambda u: "/users/%s/" % u.username,
# }

# ---------------------------------------------------------------
# Власні глобальні параметри для етапу розробки:

# Умова, при якій друкує trace_print(*args) з koopsite.functions
# TRACE_CONDITION = True
TRACE_CONDITION = False

# Умова для декоратора @unittest.skipIf(SKIP_TEST)
SKIP_TEST = True    # пропускаємо задекоровані тести
# SKIP_TEST = False   # виконуємо всі тести

if SKIP_TEST:
    print('SKIP_TEST =', SKIP_TEST)

# Умова для тестів, які потребують візуального спостереження
# WAIT_VISUAL_TEST = True    # чекати на Enter key вкінці "візуальних" тестів
WAIT_VISUAL_TEST = False    # обходити Enter key вкінці "візуальних" тестів

if WAIT_VISUAL_TEST:
    print('WAIT_VISUAL_TEST =', WAIT_VISUAL_TEST)
    print('Деякі "візуальні" тести чекатимуть на натискання ENTER в консолі')

# Якщо запущено всі тести:
if sys.argv == ['C:/PyPrograms/Django/koopsite/manage-test.py']\
        or sys.argv == ['manage.py', 'test']:
    SKIP_TEST = False
    print('SKIP_TEST =', SKIP_TEST)

# PYTHON_ANYWHERE = True  # для роботи Selenium на pythonanywhere.com
PYTHON_ANYWHERE = False # для роботи Selenium на localhost

# print('BASE_DIR=',BASE_DIR)

