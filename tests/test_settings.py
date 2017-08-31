"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = '1%qqd-$#&)#o0#2jf-o0)u76kl#)yip99b%@$f!407)jw-@#*v'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '1%qqd-$#&)#o0#2jf-o0)u76kl#)yip99b%@$f!407)jw-@#*v'
#
# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#
# TEMPLATE_DEBUG = True


# Application definition


# ROOT_URLCONF = 'job_distribution_service.urls'

# WSGI_APPLICATION = 'wsgi.application'




# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TIME_ZONE = 'Asia/Calcutta'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests',
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


DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:'
}}

PASSWORD_HASHERS=(
    'django.contrib.auth.hashers.MD5PasswordHasher',
)