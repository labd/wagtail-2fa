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

    # These URLs do not require verification if the user has no devices
    _allowed_url_names_no_device = [
        "wagtail_2fa_device_list",
        "wagtail_2fa_device_new",
        "wagtail_2fa_device_qrcode",
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

        # Don't require verification for specified paths
        if request.path in self._get_paths(self._allowed_url_names):
            return False

        # If the user does not have a device, don't require verification
        # for the specified paths
        allowed_no_device_paths = self._get_paths(self._allowed_url_names_no_device)
        if request.path in allowed_no_device_paths:
            user_has_device = django_otp.user_has_device(user, confirmed=True)
            if not user_has_device:
                return False

        # For all other cases require that the user is verfied via otp
        return True

    def _get_paths(self, route_names):
        results = []
        for route_name in route_names:
            try:
                results.append(settings.WAGTAIL_MOUNT_PATH + reverse(route_name))
            except NoReverseMatch:
                pass
        return results
