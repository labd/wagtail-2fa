from django.test import override_settings
from django.urls import NoReverseMatch, reverse
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


def test_adding_new_device_requires_verification_when_user_has_device(rf, superuser, settings, django_assert_num_queries):
    TOTPDevice.objects.create(user=superuser, confirmed=True)

    with django_assert_num_queries(2):
        url_new_device = reverse('wagtail_2fa_device_new')
        url_auth = reverse('wagtail_2fa_auth')
        request = rf.get(url_new_device)
        request.user = superuser

        middleware = VerifyUserMiddleware(lambda x: x)
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            response = middleware(request)

        assert response.url == f"{url_auth}?next={url_new_device}"


def test_adding_new_device_does_not_require_verification_when_user_has_no_device(rf, superuser, settings, django_assert_num_queries):
    with django_assert_num_queries(1):
        url_new_device = reverse('wagtail_2fa_device_new')
        url_auth = reverse('wagtail_2fa_auth')
        request = rf.get(url_new_device)
        request.user = superuser

        middleware = VerifyUserMiddleware(lambda x: x)
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            response = middleware(request)

        assert response is request


def test_get_paths(settings):
    middleware = VerifyUserMiddleware(lambda x: x)
    route_names = middleware._allowed_url_names_no_device

    expected_paths = []
    for route_name in route_names:
        try:
            expected_paths.append(settings.WAGTAIL_MOUNT_PATH + reverse(route_name))
        except NoReverseMatch:
            pass

    # Make sure non-existing paths don't get added
    route_names.append("/non/existing/path/")
    paths = middleware._get_paths(route_names)

    assert paths == expected_paths


def test_not_specifiying_wagtail_mount_point_does_not_prepend_allowed_paths_with_wagtail_mount_path(settings):
    settings.WAGTAIL_MOUNT_PATH = ''
    route_names = VerifyUserMiddleware()._allowed_url_names
    allowed_paths = VerifyUserMiddleware()._get_paths(route_names)

    for allowed_path in allowed_paths:
        assert allowed_path.startswith('/cms')


def test_specifiying_wagtail_mount_point_does_prepend_allowed_paths_with_wagtail_mount_path(settings):
    settings.WAGTAIL_MOUNT_PATH = '/wagtail'
    route_names = VerifyUserMiddleware()._allowed_url_names
    allowed_paths = VerifyUserMiddleware()._get_paths(route_names)

    for allowed_path in allowed_paths:
        assert allowed_path.startswith(settings.WAGTAIL_MOUNT_PATH)
