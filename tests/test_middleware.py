import pytest
from django.contrib.auth.models import Permission
from django.test import override_settings
from django.urls import reverse
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice

from wagtail_2fa.middleware import (
    VerifyUserMiddleware, VerifyUserPermissionsMiddleware)


def test_verified_request(rf, superuser):
    request = rf.get("/admin/")
    request.user = superuser
    device = TOTPDevice.objects.create(user=superuser, confirmed=True)
    otp_login(request, device)

    middleware = VerifyUserMiddleware()
    response = middleware.process_request(request)
    assert response is None


def test_superuser_force_mfa_auth(rf, superuser):
    request = rf.get("/admin/")
    request.user = superuser
    TOTPDevice.objects.create(user=superuser, confirmed=True)

    middleware = VerifyUserMiddleware(lambda x: x)
    with override_settings(WAGTAIL_2FA_REQUIRED=True):
        response = middleware(request)
    assert response.url == "%s?next=/admin/" % reverse("wagtail_2fa_auth")


def test_superuser_require_register_device(rf, superuser):
    request = rf.get("/admin/")
    request.user = superuser
    middleware = VerifyUserMiddleware(lambda x: x)
    with override_settings(WAGTAIL_2FA_REQUIRED=True):
        response = middleware(request)
    assert response.url == "%s?next=/admin/" % reverse("wagtail_2fa_device_new")


def test_superuser_dont_require_register_device(rf, superuser, settings):
    settings.WAGTAIL_2FA_REQUIRED = False

    request = rf.get("/admin/")
    request.user = superuser

    middleware = VerifyUserMiddleware(lambda x: x)
    response = middleware.process_request(request)
    assert response is None


def test_adding_new_device_requires_verification_when_user_has_device(
    rf, superuser, settings, django_assert_num_queries
):
    TOTPDevice.objects.create(user=superuser, confirmed=True)

    with django_assert_num_queries(2):
        url_new_device = reverse("wagtail_2fa_device_new")
        url_auth = reverse("wagtail_2fa_auth")
        request = rf.get(url_new_device)
        request.user = superuser

        middleware = VerifyUserMiddleware(lambda x: x)
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            response = middleware(request)

        assert response.url == f"{url_auth}?next={url_new_device}"


def test_adding_new_device_does_not_require_verification_when_user_has_no_device(
    rf, superuser, settings, django_assert_num_queries
):
    with django_assert_num_queries(1):
        url_new_device = reverse("wagtail_2fa_device_new")
        reverse("wagtail_2fa_auth")
        request = rf.get(url_new_device)
        request.user = superuser

        middleware = VerifyUserMiddleware(lambda x: x)
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            response = middleware(request)

        assert response is request


@pytest.mark.skip
def test_always_require_verification_when_user_has_device(rf, user, settings):
    TOTPDevice.objects.create(user=user, confirmed=True)

    url_auth = reverse("wagtail_2fa_auth")
    request = rf.get("/admin/")
    request.user = user

    middleware = VerifyUserMiddleware(lambda x: x)
    with override_settings(WAGTAIL_2FA_REQUIRED=True):
        response = middleware(request)

    assert response.url == f"{url_auth}?next=/admin/"


class TestVerifyUserPermissionsMiddleware:
    def test_enable_2fa_permission_does_require_verification(self, rf, staff_user):
        enable_2fa_permission = Permission.objects.get(codename="enable_2fa")
        user_no_2fa = staff_user
        user_no_2fa.user_permissions.add(enable_2fa_permission)

        request = rf.get("/admin/")
        request.user = user_no_2fa
        middleware = VerifyUserPermissionsMiddleware(lambda x: x)

        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            result = middleware._require_verified_user(request)

        assert result is True

    def test_no_enable_2fa_permission_no_device_does_not_require_verification(
        self, rf, staff_user
    ):
        user_2fa = staff_user

        request = rf.get("/admin/")
        request.user = user_2fa
        middleware = VerifyUserPermissionsMiddleware(lambda x: x)

        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            result = middleware._require_verified_user(request)

        assert result is False

    def test_no_enable_2fa_permission_with_device_does_require_verification(
        self, rf, staff_user
    ):
        user_2fa = staff_user
        TOTPDevice.objects.create(user=user_2fa, confirmed=True)

        request = rf.get("/admin/")
        request.user = user_2fa
        middleware = VerifyUserPermissionsMiddleware(lambda x: x)

        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            result = middleware._require_verified_user(request)

        assert result is True

    def test_process_request_enable_2fa_permission_sets_attribute_on_user_to_true(
        self, rf, staff_user
    ):
        enable_2fa_permission = Permission.objects.get(codename="enable_2fa")
        user_no_2fa = staff_user
        user_no_2fa.user_permissions.add(enable_2fa_permission)

        request = rf.get("/admin/")
        request.user = user_no_2fa
        middleware = VerifyUserPermissionsMiddleware(lambda x: x)

        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            middleware.process_request(request)

        assert request.user.enable_2fa is True

    def test_process_no_request_enable_2fa_permission_sets_attribute_on_user_to_false(
        self, rf, staff_user
    ):
        user_2fa = staff_user

        request = rf.get("/admin/")
        request.user = user_2fa
        middleware = VerifyUserPermissionsMiddleware(lambda x: x)

        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            middleware.process_request(request)

        assert request.user.enable_2fa is False
