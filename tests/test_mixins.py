import pytest
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from django.urls import reverse
from django_otp import user_has_device
from django_otp.middleware import OTPMiddleware as _OTPMiddleware
from django_otp.plugins.otp_totp.models import TOTPDevice

from wagtail_2fa.mixins import OtpRequiredMixin


class TestOtpRequiredMixin:
    def test_handle_no_permission_raises_if_authenticated(self, rf, user):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            request = rf.get("/admin/")
            request.user = user

            mixin = OtpRequiredMixin()

            with pytest.raises(PermissionDenied):
                mixin.handle_no_permission(request)

    def test_handle_no_permission_redirects_to_login_if_not_authenticated(self, rf):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            request = rf.get("/admin/")

            mixin = OtpRequiredMixin()
            response = mixin.handle_no_permission(request)
            assert response.status_code == 302
            assert response.url == "/accounts/login/?next=/admin/"

    def test_handle_no_permission_redirects_to_auth_if_user_has_device(self, rf, user):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            TOTPDevice.objects.create(user=user, confirmed=True)
            request = rf.get("/admin/")
            request.user = user

            mixin = OtpRequiredMixin()
            response = mixin.handle_no_permission(request)
            assert response.status_code == 302

            url_auth = reverse("wagtail_2fa_auth")
            assert response.url == f"{url_auth}?next=/admin/"

    def test_user_allowed_with_verified_user_returns_true(self, rf, verified_user):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            user = verified_user

            mixin = OtpRequiredMixin()
            result = mixin.user_allowed(user)
            assert result is True

    def test_user_allowed_when_no_device_and_if_configured_returns_true(self, rf, user):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            request = rf.get("/admin/")
            request.user = user
            middleware = _OTPMiddleware()
            user = middleware._verify_user(request, user)
            assert not user_has_device(user)
            assert user.is_authenticated

            mixin = OtpRequiredMixin()
            mixin.if_configured = True
            result = mixin.user_allowed(user)
            assert result is True
