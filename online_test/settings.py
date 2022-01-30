"""
Django settings for online_test project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from yaksh.pipeline.settings import AUTH_PIPELINE
import os
from decouple import config
from django.utils.translation import ugettext_lazy as _
from machina import MACHINA_MAIN_TEMPLATE_DIR
from machina import MACHINA_MAIN_STATIC_DIR


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# The directory where user data can be saved.  This directory will be
# world-writable and all user code will be written and saved here by the
# code server with each user having their own sub-directory.
OUTPUT_DIR = os.path.join(BASE_DIR, "yaksh_data", "output")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='dUmMy_s3cR3t_k3y')

#rediretcion
SECURE_SSL_REDIRECT = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','iziklasse.net','www.iziklasse.net']

# This is a required field
DOMAIN_HOST = "http://127.0.0.1:8000"

URL_ROOT = ''

# Application definition

INSTALLED_APPS = (
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yaksh',
    'taggit',
    'social_django',
    'grades',
    'stats',
    'django_celery_beat',
    'django_celery_results',
    'notifications_plugin',
    'rest_framework',
    'api',
    'corsheaders',
    'rest_framework.authtoken',
    'storages',
    "translation_manager",
    # Machina dependencies:
    'mptt',
    'haystack',
    'widget_tweaks',
    # Machina apps:
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',
    'highlightjs',
    'rquiz',
    'qcm',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'yaksh.middleware.one_session_per_user.OneSessionPerUserMiddleware',
    'yaksh.middleware.get_notifications.NotificationMiddleware',
    'yaksh.middleware.user_time_zone.TimezoneMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    'django.middleware.security.SecurityMiddleware'
)

ROOT_URLCONF = 'online_test.urls'

WSGI_APPLICATION = 'online_test.wsgi.application'

context_processors = [
    'django.template.context_processors.media', # set this explicitly
]
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{0}'.format(
            config('mysql', default='sqlite3')
        ),
        'NAME': config('fwpa6521_iziklasse2',
                       default=os.path.join(BASE_DIR, 'db.sqlite3')
                       ),
        # The following settings are not used with sqlite3:
        'USER': config('fwpa6521_iziklasse2', default='fwpa6521_iziklasse2'),
        'PASSWORD': config('6rJkNTiG5f6p4JF', default='6rJkNTiG5f6p4JF'),
        # Empty for localhost through domain sockets or '1$
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=''),
    },
}"""
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'fwpa6521_iziklasse2',
        'USER':'fwpa6521_iziklasse2',
        'PASSWORD':'6rJkNTiG5f6p4JF',
        'HOST':'localhost',
        'PORT':'3306'
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'online_test/locale'),  # base folder where manage.py resides
    os.path.join(BASE_DIR, 'grades/locale'),  # app folder
    os.path.join(BASE_DIR, 'yaksh/locale'),
    #os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'stats/locale')
]

LANGUAGES = [
   ('en', _('English')),
   ('fr', _('French')),
   ('es',_('Spanish')),
   ('pt',_('Spanish')),
   ('de',_('Spanish')),
   ('ko',_('Spanish')),
   ('hu',_('Spanish')),
   ('pl',_('Spanish')),
   #('wo',_('Spanish')),
   ('ca',_('Spanish')),
   ('el',_('Spanish')),
   ('id',_('Spanish')),
   ('it',_('Spanish')),
   ('nl',_('Spanish')),
   ('pt',_('Spanish')),
   ('ru',_('Spanish')),
   ('th',_('Spanish')),
   ('ar',_('Spanish')),
   ('be',_('Spanish')),
   ('bg',_('Spanish')),
   ('bn',_('Spanish')),
   ('et',_('Spanish')),
   ('eu',_('Spanish')),
   #('fil',_('Spanish')),
   ('he',_('Spanish')),
   ('hi',_('Spanish')),
   ('hu',_('Spanish')),
   ('ja',_('Spanish')),
   ('lb',_('Spanish')),
   ('sl',_('Spanish')),
   ('sv',_('Spanish')),
   ('tr',_('Spanish')),
   ('vi',_('Spanish')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/exam/login/'

LOGIN_REDIRECT_URL = '/exam/'

SOCIAL_AUTH_LOGIN_ERROR_URL = '/exam/login/'

MEDIA_URL = "/data/"

MEDIA_ROOT = os.path.join(BASE_DIR, "yaksh_data", "data")

STATIC_ROOT = 'yaksh/static/'

# Set this varable to <True> if smtp-server is not allowing to send email.
EMAIL_USE_TLS = False

EMAIL_HOST = 'your_email_host'

EMAIL_PORT = 'your_email_port'

EMAIL_HOST_USER = 'email_host_user'

EMAIL_HOST_PASSWORD = 'email_host_password'

# Set EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend'
# in production
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# SENDER_EMAIL, REPLY_EMAIL, PRODUCTION_URL, IS_DEVELOPMENT are used in email
# verification. Set the variables accordingly to avoid errors in production

# This email id will be used as <from address> for sending emails.
# For example no_reply@<your_organization>.in can be used.
SENDER_EMAIL = 'your_email'

# Organisation/Indivudual Name.
SENDER_NAME = 'your_name'

# This email id will be used by users to send their queries
# For example queries@<your_organization>.in can be used.
REPLY_EMAIL = 'your_reply_email'

# This url will be used in email verification to create activation link.
# Add your hosted url to this variable.
# For example https://127.0.0.1:8000 or 127.0.0.1:8000
PRODUCTION_URL = 'your_project_url'

# Set this variable to <False> once the project is in production.
# If this variable is kept <True> in production, email will not be verified.
IS_DEVELOPMENT = True

# Video File upload size
MAX_UPLOAD_SIZE = 524288000


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STATICFILES_DIRS = (
    # ...
    BASE_DIR+"/static",
    MACHINA_MAIN_STATIC_DIR,
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'APP_DIRS': True,
        'DIRS': ['yaksh/templates', MACHINA_MAIN_TEMPLATE_DIR],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'machina.core.context_processors.metadata'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': True,  # make this False in production
        }
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'GOOGLE_KEY_PROVIDED'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'GOOGLE_SECRET_PROVIDED'

SOCIAL_AUTH_FACEBOOK_KEY = 'FACEBOOK_KEY_PROVIDED'
SOCIAL_AUTH_FACEBOOK_SECRET = 'FACEBOOK_SECRET_PROVIDED'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = AUTH_PIPELINE

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

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
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TAGGIT_CASE_INSENSITIVE = True


# Celery parameters
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'django-db'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



# AWS Credentials
USE_AWS = False
if USE_AWS:
    AWS_ACCESS_KEY_ID = "access-key"
    AWS_SECRET_ACCESS_KEY = "secret-key"
    AWS_S3_REGION_NAME = "ap-south-1"
    AWS_STORAGE_BUCKET_NAME = "yaksh-django"
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = "virtual"

    # Static Location
    AWS_STATIC_LOCATION = 'static'
    STATICFILES_STORAGE = 'yaksh.storage_backends.StaticStorage'
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
    # Media Public
    AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
    DEFAULT_FILE_STORAGE = 'yaksh.storage_backends.PublicMediaStorage'

