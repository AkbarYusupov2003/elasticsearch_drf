from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-cde=vfrkae5pf@2x_*gp=80c3om!qk%2^r&*ti@34qbb9@ow1='

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    "rest_framework",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    # my apps
    "search",
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "content_search_drf", #"new_content_search_drf",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

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

LANGUAGE_CODE = "en"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

ELASTICSEARCH__USERNAME = "elastic"
ELASTICSEARCH__PASSWORD = "ml0LOVWEX14gs8nvrqi="
ELASTICSEARCH__HOST_IP = "localhost"
ELASTICSEARCH__HOST_PORT = "9200"

# kibana_system 5lxxtxeqqYa+mHbgFKcr

# bin/elasticsearch-reset-password.bat -u elastic

ELASTICSEARCH_URL = f'elasticsearch://{ELASTICSEARCH__USERNAME}:{ELASTICSEARCH__PASSWORD}@{ELASTICSEARCH__HOST_IP}:{ELASTICSEARCH__HOST_PORT}'

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": ELASTICSEARCH_URL
    },
    
}

ELASTICSEARCH_INDEX_NAMES = {
    "search.movie": "movies",
}
