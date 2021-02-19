import os
import logging
import environ

logger = logging.getLogger(__name__)
env = environ.Env()
env.read_env(env.str('./', '.env'))

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = bool(env('DEBUG'))

ALLOWED_HOSTS = ['*']

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

    'miet_union',
    'documents',
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

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# admin_tools settings
ADMIN_TOOLS_INDEX_DASHBOARD = 'miet_union.dashboard.CustomIndexDashBoard'

AUTH_USER_MODEL = 'miet_union.User'

# for summernote
X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']