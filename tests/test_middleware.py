from django.test import override_settings
from django.urls import reverse
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice

from wagtail_2fa.middleware import VerifyUserMiddleware


def test_verified_request(rf, superuser):
    request = rf.get('/admin/')
    request.user = superuser
    device = TOTPDevice.objects.create(user=superuser, confirmed=True)
    otp_login(request, device)

    middleware = VerifyUserMiddleware()
    response = middleware.process_request(request)
    assert response is None


def test_superuser_force_mfa_auth(rf, superuser):
    request = rf.get('/admin/')
    request.user = superuser
    TOTPDevice.objects.create(user=superuser, confirmed=True)

    middleware = VerifyUserMiddleware(lambda x: x)
    with override_settings(WAGTAIL_2FA_REQUIRED=True):
        response = middleware(request)
    assert response.url == '%s?next=/admin/' % reverse('wagtail_2fa_auth')


def test_superuser_require_register_device(rf, superuser):
    request = rf.get('/admin/')
    request.user = superuser
    middleware = VerifyUserMiddleware(lambda x: x)
    with override_settings(WAGTAIL_2FA_REQUIRED=True):
        response = middleware(request)
    assert response.url == '%s?next=/admin/' % reverse('wagtail_2fa_device_new')


def test_superuser_dont_require_register_device(rf, superuser, settings):
    settings.WAGTAIL_2FA_REQUIRED = False

    request = rf.get('/admin/')
    request.user = superuser

    middleware = VerifyUserMiddleware(lambda x: x)
    response = middleware.process_request(request)
    assert response is None


def test_not_specifiying_wagtail_mount_point_does_not_prepend_allowed_paths_with_wagtail_mount_path(settings):
    settings.WAGTAIL_MOUNT_PATH = ''
    allowed_paths = VerifyUserMiddleware()._allowed_paths

    for allowed_path in allowed_paths:
        assert allowed_path.startswith('/cms')


def test_specifiying_wagtail_mount_point_does_prepend_allowed_paths_with_wagtail_mount_path(settings):
    settings.WAGTAIL_MOUNT_PATH = '/wagtail'
    allowed_paths = VerifyUserMiddleware()._allowed_paths

    for allowed_path in allowed_paths:
        assert allowed_path.startswith(settings.WAGTAIL_MOUNT_PATH)
