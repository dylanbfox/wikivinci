from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# we only need the engine name, as heroku takes care of the rest
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

# # Allow all host hosts/domain names for this site
ALLOWED_HOSTS = ['limitless-temple-7879.herokuapp.com', 'www.wikivinci.com']

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default' : dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Media settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL
# necessary for thumbnails to be stored on S3 and not in local memory!
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Celery settings
BROKER_POOL_LIMIT = None
BROKER_URL = os.environ["CLOUDAMQP_URL"]

# Email settings
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Leonardo da Wikivinci <leo@wikivinci.com>"
SERVER_EMAIL = '[PROD] error@wikivinci.com <error@wikivinci.com>'

# Misc. settings
HOST_NAME = 'http://www.wikivinci.com'