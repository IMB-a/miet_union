"""
Django settings for miet_union project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import logging

logger = logging.getLogger(__name__)

try:
    from miet_union.email_config import (
        EMAIL_HOST,
        EMAIL_PORT,
        EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD,
        EMAIL_USE_TLS,
        EMAIL_USE_SSL,
    )
    EMAIL_HOST = EMAIL_HOST
    EMAIL_PORT = EMAIL_PORT
    EMAIL_HOST_USER = EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
    EMAIL_USE_SSL = EMAIL_USE_SSL
    EMAIL_USE_TLS = EMAIL_USE_TLS
except ImportError:
    logger.error('email_config ImportError')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'plq@i)*#1wt5=6ukm#i3no+xf%v-3!e7r7p-8oxmi+f^nz!j@i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["hearthstowner.pythonanywhere.com"]


# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_summernote',
    # our apps
    'miet_union',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miet_union.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'miet_union.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',    # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# admin_tools settings
ADMIN_TOOLS_INDEX_DASHBOARD = 'miet_union.dashboard.CustomIndexDashBoard'

AUTH_USER_MODEL = 'miet_union.User'
