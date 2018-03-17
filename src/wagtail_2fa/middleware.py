from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from django_otp.middleware import OTPMiddleware as _OTPMiddleware


class VerifyUserMiddleware(_OTPMiddleware):

    def process_request(self, request):
        super().process_request(request)
        if (
            request.user.is_authenticated
            and not request.user.is_verified()
            and self._require_verified_user(request)
        ):
            return redirect_to_login(
                 request.get_full_path(),
                 login_url=reverse('wagtail_2fa_auth'))

    def _require_verified_user(self, request):
        if request.path == reverse('wagtail_2fa_auth'):
            return False
        return True
