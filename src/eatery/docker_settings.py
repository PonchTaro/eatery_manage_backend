from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eatery',
        'USER': 'develop',
        'PASSWORD': 'test',
        'HOST': 'db',
        'PORT': '5432',
    },
}

# ここにVISIT_URLを改造したものをコマンドから追加