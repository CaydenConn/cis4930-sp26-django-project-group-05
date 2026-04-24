from decouple import config

from .base import *

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-only-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [
    host.strip()
    for host in config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
    if host.strip()
]
