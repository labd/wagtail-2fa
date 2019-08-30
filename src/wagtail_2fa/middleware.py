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
        if request.path in self._allowed_paths:
            return False

        # For all other cases require that the user is verfied via otp
        return True

    @property
    def _allowed_paths(self):
        """Return the paths the user may visit when not verified via otp

        This result cannot be cached since we want to be compatible with the
        django-hosts package. Django-hosts alters the urlconf based on the
        hostname in the request, so the urls might exist for admin.<domain> but
        not for www.<domain>.

        """
        results = []
        for route_name in self._allowed_url_names:
            try:
                results.append(settings.WAGTAIL_MOUNT_PATH + reverse(route_name))
            except NoReverseMatch:
                pass
        return results
