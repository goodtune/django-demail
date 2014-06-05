from os.path import dirname, join as basejoin, realpath

join = lambda *args: realpath(basejoin(*args))

PROJECT_DIR = join(dirname(__file__), '..')
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-AU'

USE_TZ = True
STATIC_URL = '/static/'

SECRET_KEY = ')l+649%yw_so!5twpu1-e&amp;b(2ldpswad9_*vdc8t@de4)h@n4j'

ROOT_URLCONF = 'test_app.urls'
WSGI_APPLICATION = 'test_app.wsgi.application'

INSTALLED_APPS = (
    'demail',
)

# Critical that the DEMAIL_BACKEND defaults to LocMem as this is what the test
# environment will expect. Inspecting the ``mail.outbox`` in tests will fail
# if the test case uses a different backend.
DEMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)-10s %(name)-30s %(asctime)-27s '
                      '%(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'demail': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}
