"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-part packages
    'rest_framework',
    'crispy_forms',
    'markdown_deux',
    'widget_tweaks',
    'django_celery_beat',
    'django_celery_results',
    'rangefilter',
    'tracking',
    'ckeditor',
    'suit',
    'tagulous',

    # All-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Logger
    'django_db_logger',
    'logs',

    # Local apps
    'accounts',
    'configs',
    'crops',
    'rices',
    'fruits',
    'flowers',
    'hogs',
    'rams',
    'chickens',
    'ducks',
    'gooses',
    'seafoods',
    'cattles',
    'dailytrans',
    'watchlists',
    'posts',
    'comments',
    'events',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
]

ROOT_URLCONF = 'dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.ga_tracking_id',
                'dashboard.context_processors.use_ga'
            ],
        },
    },
]

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
        'aprp_log': {
            'level': 'DEBUG',
            'class': 'logs.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
        'aprp': {
            'handlers': ['aprp_log'],
            'level': 'DEBUG'
        }
    }
}


# Database

# Sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

# Local time zone for this installation. All choices can be found here:
# https://en.wikipedia.org/wiki/List_of_tz_zones_by_name (although not all
# systems may support all possibilities). When USE_TZ is True, this is
# interpreted as the default user time zone.
TIME_ZONE = 'Asia/Taipei'

# If you set this to True, Django will use timezone-aware datetimes
# .
USE_TZ = True

# Languages we provide translations for, out of the box.
LANGUAGES = [
    ('zh-hant', _('Traditional Chinese')),
    ('en', _('English')),
]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


# Settings for language cookie
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'


# If you set this to True, Django will format dates, numbers and calendars
# according to user current locale.
USE_L10N = False


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_URL = '/static/'

# WhiteNoise

STATIC_ROOT = os.path.join(BASE_DIR, "live-static-files", "static-root")
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "live-static-files", "media-root")

SERVE_MEDIA_FILES = False  # make whitenoise serving media files

# All-auth

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Crispy

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Fixtures

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
    os.path.join(BASE_DIR, 'fixtures/rices'),
    os.path.join(BASE_DIR, 'fixtures/crops'),
    os.path.join(BASE_DIR, 'fixtures/crops/origin'),
    os.path.join(BASE_DIR, 'fixtures/crops/wholesale'),
    os.path.join(BASE_DIR, 'fixtures/fruits'),
    os.path.join(BASE_DIR, 'fixtures/fruits/origin'),
    os.path.join(BASE_DIR, 'fixtures/fruits/wholesale'),
    os.path.join(BASE_DIR, 'fixtures/flowers/wholesale'),
    os.path.join(BASE_DIR, 'fixtures/hogs'),
    os.path.join(BASE_DIR, 'fixtures/rams'),
    os.path.join(BASE_DIR, 'fixtures/chickens'),
    os.path.join(BASE_DIR, 'fixtures/ducks'),
    os.path.join(BASE_DIR, 'fixtures/gooses'),
    os.path.join(BASE_DIR, 'fixtures/seafoods/origin'),
    os.path.join(BASE_DIR, 'fixtures/seafoods/wholesale'),
    os.path.join(BASE_DIR, 'fixtures/cattles'),
    os.path.join(BASE_DIR, 'fixtures/watchlists'),
    os.path.join(BASE_DIR, 'fixtures/events'),
]

# Rest-framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DATE_INPUT_FORMATS": ["%Y/%m/%d"],
}

# Celery

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_IMPORTS = (
    'dashboard.tasks',
    'rices.tasks',
    'crops.tasks',
    'fruits.tasks',
    'hogs.tasks',
    'rams.tasks',
    'chickens.tasks',
    'ducks.tasks',
    'gooses.tasks',
    'seafoods.tasks',
    'cattles.tasks',
    'watchlists.tasks',
)

# Session Settings
SESSION_COOKIE_AGE = 7200

# Google Analytics
USE_GA = False
GA_TRACKING_ID = ''

# Password limits
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]