import os

# local variables read into settings.py. 
# variables set here will override whatever's in settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG=True
ALLOWED_HOSTS = ['localhost',]

FILE_SYSTEM_BASE = os.path.join(BASE_DIR, 'baked_site')
USE_TZ = True
TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_ROOT,],
        'APP_DIRS': False,
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
