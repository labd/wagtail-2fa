import django_otp
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from django_otp.middleware import OTPMiddleware as _OTPMiddleware


class VerifyUserMiddleware(_OTPMiddleware):
    _allowed_url_names = [
        'wagtail_2fa_auth',
        'wagtail_2fa_device_list',
        'wagtail_2fa_device_new',
        'wagtail_2fa_device_qrcode',
        'wagtailadmin_login',
        'wagtailadmin_logout',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_paths = [reverse(n) for n in self._allowed_url_names]

    def process_request(self, request):
        super().process_request(request)
        user = request.user

        if self._require_verified_user(request):
            user_has_device = django_otp.user_has_device(user, confirmed=True)

            if user_has_device and not user.is_verified():
                return redirect_to_login(
                    request.get_full_path(),
                    login_url=reverse('wagtail_2fa_auth'))

            elif not user_has_device and settings.WAGTAIL_2FA_REQUIRED:
                # only allow the user to visit the admin index page and the
                # admin setup page
                return redirect_to_login(
                    request.get_full_path(),
                    login_url=reverse('wagtail_2fa_device_new'))

    def _require_verified_user(self, request):
        user = request.user

        if not user.is_authenticated:
            return False

        # If the user has no access to the admin anyway then don't require a
        # verified user here
        if not (
            user.is_staff or user.is_superuser or
            user.has_perms(['wagtailadmin.access_admin'])
        ):
            return False

        # Allow the user to a fixed number of paths when not verified
        if request.path in self._allowed_paths:
            return False

        # For all other cases require that the user is verfied via otp
        return True
