from decouple import config

from api.configparser import getTokenExpirationTime

__all__ = ['MONGODB_URI', 'JWT_SECRET_KEY', 'DEBUG', 'JWT_COOKIE_SECURE',
           'JWT_ACCESS_TOKEN_EXPIRES', 'JWT_REFRESH_TOKEN_EXPIRES', 'PROPAGATE_EXCEPTIONS']


DEBUG = config('DEBUG')
MONGODB_URI = config('MONGODB_URI')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_COOKIE_SECURE = config('JWT_COOKIE_SECURE')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = getTokenExpirationTime(
    int(config('JWT_ACCESS_TOKEN_EXPIRES')))
JWT_REFRESH_TOKEN_EXPIRES = getTokenExpirationTime(
    int(config('JWT_REFRESH_TOKEN_EXPIRES')))
PROPAGATE_EXCEPTIONS = config('PROPAGATE_EXCEPTIONS')
