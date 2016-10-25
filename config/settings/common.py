# -*- coding: utf-8 -*-
"""
Django settings for exo_sketchfab project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import datetime
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (exo_sketchfab/config/settings/common.py - 3 = exo_sketchfab/)
APPS_DIR = ROOT_DIR.path('exo_sketchfab')

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts

    # https://github.com/pennersr/django-allauth
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.facebook',

    # https://github.com/tomchristie/django-rest-framework/tree/master
    'rest_framework',

    # django-rest-auth
    # https://github.com/Tivix/django-rest-auth/blob/master/docs/installation.rst
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    # Django-rest-swagger
    # http://django-rest-swagger.readthedocs.io/en/latest/
    'rest_framework_swagger',

    # Django-friendship
    # https://github.com/revsys/django-friendship
    'friendship',

)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'exo_sketchfab.users.apps.UsersConfig',


    # Your stuff: custom apps go here
    'exo_sketchfab.socialaccounts',
    'exo_sketchfab.friendships',
    'exo_sketchfab.models3d',
    'exo_sketchfab.badges',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'exo_sketchfab.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Leo Maltrait""", 'leo.maltrait.job@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///exo_sketchfab'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

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

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
#ACCOUNT_AUTHENTICATION_METHOD = 'username'
#ACCOUNT_EMAIL_REQUIRED = True
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'exo_sketchfab.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'exo_sketchfab.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'







# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

#####################################
# DJANGO ALL AUTH (see default above)
# http://django-allauth.readthedocs.io/en/latest/configuration.html

#  The name of the field containing the username, if any. See custom user models. 'None' is possible/
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # auth either with email or username
#  Change to false if you don't want it to be required after signing up
ACCOUNT_EMAIL_VERIFICATION = 'optional'

ACCOUNT_ADAPTER = 'exo_sketchfab.users.adapters.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'exo_sketchfab.users.adapters.SocialAccountAdapter'

SOCIALACCOUNT_AUTO_SIGNUP = True

#  in dev facebook > settings > advanced: http://localhost:8000/accounts/facebook/login/callback/
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        #'AUTH_PARAMS': {'auth_type': 'https'},

        # Infos asked to Facebook
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'picture',
            'timezone',
            'link',
            'gender',
            'updated_time',
            'friends'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.4'}}



#####################################
# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (

        # Don't use cookies by default (else 403 when POST/PUT/DELETE)
        #'rest_framework.authentication.SessionAuthentication',

        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

}

#####################################
# Django REST Framework-JWT

JWT_AUTH = {

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'config.settings.utils.jwt_response_payload_handler',

    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),

    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

}

#####################################
# Django-REST-AUTH
# https://github.com/Tivix/django-rest-auth/blob/master/docs/installation.rst

REST_USE_JWT = True # Use JWT with django-rest-auth instead of auth token (django token)
#REST_SESSION_LOGIN = False

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'exo_sketchfab.users.serializers.RegisterSerializer',
}
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'exo_sketchfab.users.serializers.UserDetailsSerializer',

    'JWT_SERIALIZER': 'exo_sketchfab.users.serializers.JWTSerializer',
}



#####################################
# Django-rest-swagger
# http://django-rest-swagger.readthedocs.io/en/latest/
# http://marcgibbons.github.io/django-rest-swagger/settings/

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}


