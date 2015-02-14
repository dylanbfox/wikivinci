from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += (
	'debug_toolbar',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "wikivinci",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Celery
BROKER_URL = 'amqp://myuser:password@localhost:5672/myvhost'
CELERY_ALWAYS_EAGER = False

if CELERY_ALWAYS_EAGER:
	print "*************************"
	print "[WARNING] CELERY_ALWAYS_EAGER is set to True!"
	print "*************************"	

# Email settings
EMAIL_HOST = "smtp.gmail.com" # gmail on local
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME'] # gmail on local
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD'] # gmail on local
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Leonardo da Wikivinci <leo@wikivinci.com>"
SERVER_EMAIL = '[PROD] error@wikivinci.com <error@wikivinci.com>'

# Misc. settings
HOST_NAME = 'http://4cb45e0f.ngrok.com'