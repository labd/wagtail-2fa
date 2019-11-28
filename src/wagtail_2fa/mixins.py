from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from django_otp import user_has_device


class OtpRequiredMixin(object):
    """
    if_configured: If ``True``, an authenticated user with no confirmed
        OTP devices will be allowed. Default is ``False``.
    """

    if_configured = False

    def handle_no_permission(self, request):
        """Redirect unauthenticated users to login else raise PermissionDenied"""
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME
            )
        raise PermissionDenied

    def user_allowed(self, user):
        return user.is_verified() or (
            self.if_configured and user.is_authenticated and not user_has_device(user)
        )

    def dispatch(self, request, *args, **kwargs):

        if not self.user_allowed(request.user):
            return self.handle_no_permission(request)

        return super(OtpRequiredMixin, self).dispatch(request, *args, **kwargs)
