from django.conf import settings


def pytest_configure():
    settings.configure(
        MIDDLEWARE_CLASSES=[],
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        },
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            },
        }
    )
