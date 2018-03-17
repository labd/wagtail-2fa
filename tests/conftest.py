import pytest
from django.conf import settings


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE_CLASSES=[],
        INSTALLED_APPS=[
            'wagtail_2fa',

            'wagtail.contrib.forms',
            'wagtail.contrib.redirects',
            'wagtail.embeds',
            'wagtail.sites',
            'wagtail.users',
            'wagtail.snippets',
            'wagtail.documents',
            'wagtail.images',
            'wagtail.search',
            'wagtail.admin',
            'wagtail.core',
            'wagtail.contrib.modeladmin',

            'modelcluster',
            'taggit',
            'debug_toolbar',

            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'django_otp',
            'django_otp.plugins.otp_totp',
        ],
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


@pytest.fixture()
def rf():
    """A RequestFactory instance."""

    from django.contrib.auth.models import AnonymousUser
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.contrib.sessions.backends.db import SessionStore
    from django.test.client import RequestFactory as BaseRequestFactory

    class RequestFactory(BaseRequestFactory):

        def request(self, user=None, **request):
            request = super().request(**request)
            request.user = AnonymousUser()
            request.session = SessionStore()
            request._messages = FallbackStorage(request)
            return request

    return RequestFactory()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='test-user')


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create(
        username='super-user', is_superuser=True, is_staff=True)
