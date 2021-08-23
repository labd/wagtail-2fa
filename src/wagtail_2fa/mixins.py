from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django_otp import user_has_device


class OtpRequiredMixin(object):
    """
    if_configured: If ``True``, an authenticated user with no confirmed
        OTP devices will be allowed. Default is ``False``.
    """

    if_configured = False

    def handle_no_permission(self, request):
        """Redirect unauthenticated users."""
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME
            )

        if user_has_device(request.user):
            return redirect_to_login(
                request.get_full_path(), login_url=reverse("wagtail_2fa_auth")
            )

        raise PermissionDenied

    def user_allowed(self, user):
        if not settings.WAGTAIL_2FA_REQUIRED:
            return True

        return user.is_verified() or (
            self.if_configured and user.is_authenticated and not user_has_device(user)
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.user_allowed(request.user):
            return self.handle_no_permission(request)

        return super(OtpRequiredMixin, self).dispatch(request, *args, **kwargs)
