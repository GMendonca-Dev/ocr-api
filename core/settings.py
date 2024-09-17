from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants
import os

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [

    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    ##### Third party apps #####
    
    'easyaudit',
    'django_filters',
    'rest_framework',

    ##### Local apps  #####
    
    'ocr',
    'api',
   
]

MIDDLEWARE = [

    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Acrescentei
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {

    'default': {

      "ENGINE": "django.db.backends.postgresql",
      'NAME': os.getenv("NAME_DB"),
      'USER': os.getenv("USER_DB"),
      'PASSWORD': os.getenv("PASSWORD_DB"),
      'HOST': os.getenv("HOST_DB"),
      'PORT': os.getenv("PORT_DB"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Password Hashers

PASSWORD_HASHERS = [

    "django.contrib.auth.hashers.ScryptPasswordHasher",
    # "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    # "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    # "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    # "django.contrib.auth.hashers.Argon2PasswordHasher",
    # "django.contrib.auth.hashers.BCryptPasswordHasher",
    
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Maceio'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# ################## Curso Let
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de Login
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/accounts/login'


# Configurações do easyaudit
EASY_AUDIT_WATCH_LOGIN = True
EASY_AUDIT_WATCH_LOGOUT = True
EASY_AUDIT_WATCH_REQUEST = True
EASY_AUDIT_WATCH_USER = True
EASY_AUDIT_WATCH_ADMIN = True
EASY_AUDIT_WATCH_AUTH = True
EASY_AUDIT_WATCH_LOGIN_EVENTS = True
EASY_AUDIT_WATCH_LOGOUT_EVENTS = True
EASY_AUDIT_WATCH_REQUEST_EVENTS = True
EASY_AUDIT_WATCH_MODEL_EVENTS = True

# Mensagens
MESSAGE_TAGS = {

    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.DEBUG: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',

}


JAZZMIN_SETTINGS = {}
JAZZMIN_SETTINGS["show_ui_builder"] = True