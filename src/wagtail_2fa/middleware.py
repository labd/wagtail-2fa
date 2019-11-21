from functools import partial

import django_otp
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import NoReverseMatch, reverse
from django.utils.functional import SimpleLazyObject
from django_otp.middleware import OTPMiddleware as _OTPMiddleware


class VerifyUserMiddleware(_OTPMiddleware):
    _allowed_url_names = [
        "wagtail_2fa_auth",
        "wagtailadmin_login",
        "wagtailadmin_logout",
    ]
    _allowed_url_names_no_device = [
        "wagtail_2fa_auth",
        "wagtail_2fa_device_list",
        "wagtail_2fa_device_new",
        "wagtail_2fa_device_qrcode",
        "wagtailadmin_login",
        "wagtailadmin_logout",
    ]

    def __call__(self, request):
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        if request.user:
            request.user = SimpleLazyObject(partial(self._verify_user, request, request.user))
        user = request.user
        if self._require_verified_user(request):
            user_has_device = django_otp.user_has_device(user, confirmed=True)

            if user_has_device and not user.is_verified():
                return redirect_to_login(
                    request.get_full_path(), login_url=reverse("wagtail_2fa_auth")
                )

            elif not user_has_device and settings.WAGTAIL_2FA_REQUIRED:
                # only allow the user to visit the admin index page and the
                # admin setup page
                return redirect_to_login(
                    request.get_full_path(), login_url=reverse("wagtail_2fa_device_new")
                )

    def _require_verified_user(self, request):
        user = request.user

        if not settings.WAGTAIL_2FA_REQUIRED:
            # If two factor authentication is disabled in the settings
            return False

        if not user.is_authenticated:
            return False

        # If the user has no access to the admin anyway then don't require a
        # verified user here
        if not (
            user.is_staff
            or user.is_superuser
            or user.has_perms(["wagtailadmin.access_admin"])
        ):
            return False

        # Allow the user to a fixed number of paths when not verified
        user_has_device = django_otp.user_has_device(user, confirmed=True)
        if request.path in self._get_allowed_paths(user_has_device):
            return False

        # For all other cases require that the user is verfied via otp
        return True

    def _get_allowed_paths(self, has_device):
        """Return the paths the user may visit when not verified via otp.

        If the user already has a registered device, return a limited set of
        paths to prevent them from adding or listing devices to prevent them
        from adding or listing devices.
        """
        allowed_url_names = self._allowed_url_names
        if not has_device:
            allowed_url_names = self._allowed_url_names_no_device

        results = []
        for route_name in allowed_url_names:
            try:
                results.append(settings.WAGTAIL_MOUNT_PATH + reverse(route_name))
            except NoReverseMatch:
                pass
        return results
