# SECURITY WARNING: don't run with debug turned on in production!
from datetime import timedelta

DEBUG = True

ALLOWED_HOSTS = ["*"]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Charity Auction Project API',
    'DESCRIPTION': 'Charity Auction Project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
