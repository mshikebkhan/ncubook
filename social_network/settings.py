"""
Django settings for social_network project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'axve$8*^!n)e#nbc3&_rsz4z3^p&sm^$89--)5#75x9#m2l+!8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tz_detect', # Detect Timezone

    'django_cleanup.apps.CleanupConfig', # Cleans Files Of Deleted Models

    'ncubook',
    'users',
    'posts',
    'messenger',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware', # Detect Timezone
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static Files On Production
]

ROOT_URLCONF = 'social_network.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'social_network/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messenger.views.nav_dms_count', # Navbar Direct Messages Count
                'users.views.nav_brequests_count', # Navbar Buddy Requests Count
                'notifications.views.nav_notifications_count', # Navbar Notifications Count                
            ],
        },
    },
]

WSGI_APPLICATION = 'social_network.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Detect Timezone
TZ_DETECT_COUNTRIES = ('IN',)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# For white noise
FILE_CHARSET = "utf-8"


# For sending mails to students only
UNIVERSITY_EMAIL_DOMAIN = "@university.com"

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # When DEBUG==False

MEDIA_URL =  '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'ncubook:login'
LOGIN_REDIRECT_URL = 'ncubook:index'

# Django by default danger message's tuning.
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}

# Log the user out after certain period of time.
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # opional, as this will log you out when browser is closed
SESSION_COOKIE_AGE = 1*24*60*60          # Log out after days: 1
SESSION_SAVE_EVERY_REQUEST = False      # Will perevent from logging you out after 300 seconds
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
