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
    'base',
   
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

# ################## Estáticos

# Configuração para servir os arquivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "base", "static"),  # Aponta para a pasta 'static' dentro do app 'base'
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações de Login
# LOGIN_URL = '/accounts/login'
# LOGIN_REDIRECT_URL = '/home/'
# LOGOUT_REDIRECT_URL = '/accounts/login'


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


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-light",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "solar",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

JAZZMIN_SETTINGS = {
    # Título da aba do Admin
    "site_title": "Xpertis",

    # Nome que aparece no canto superior esquerdo
    "site_header": "Xpertis-OCR",

    # O texto que aparece ao lado da logo
    "site_brand": "Xpertis",

    # Caminho para o logo (deve estar na pasta de arquivos estáticos)
    "site_logo": "img/logo_xpertis.png",  # Substitua pelo caminho do seu logo
    

    # Caminho para o favicon (opcional)
    #"site_icon": "path/para/favicon.ico",  # Substitua pelo caminho do seu favicon

    # Use o logotipo no formulário de login
    "login_logo": "img/logo_xpertis.png",
    "login_css": "css/custom.css",
    
    # Use o logotipo nas páginas de login
    "login_logo_dark": None,  # Você pode definir um logo alternativo para tema escuro

    # Outras personalizações (se necessário)
    "welcome_sign": "Bem-vindo ao Xpertis-OCR",
    # "copyright": "Copyright © 2024 Meu Projeto",
    "copyright": "- Xpertis-OCR",
    "show_sidebar": True,

    # Definir ícones personalizados para os apps e modelos
    "icons": {
        "auth": "fas fa-users-cog",  # Ícone para o app de autenticação
        "auth.user": "fas fa-user",  # Ícone para o modelo User
        "auth.Group": "fas fa-users",  # Ícone para o modelo Group
        "ocr.DocumentosOcr": "fas fa-file-alt",  # Ícone para o modelo DocumentosOcr
        "ocr.DocumentosOcrErros": "fas fa-exclamation-triangle",  # Ícone para o modelo DocumentosOcrErros
    },


    # Definir a ordem dos apps e modelos no menu lateral
    "order_with_respect_to": {
        "ocr.documentosocr",        # Coloca o modelo DocumentosOcr primeiro
        "ocr.documentosocrerros",   # Coloca o modelo DocumentosOcrErros depois
    },


    "custom_css": "css/custom.css",
    "show_ui_builder": False,
    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"],  "model": "auth.Group"},

        # external url that opens in a new window (Permissions can be added)
        #{"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # Link para o modelo 'Group'
        {"model": "auth.Group"},  # Adiciona o link para o modelo 'Group'

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "ocr"},
    ],

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],


    "changeform_format": "horizontal_tabs",

    "language_chooser": False,

}