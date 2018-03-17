from wagtail_2fa.middleware import VerifyUserMiddleware
from django.urls import reverse
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice


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

    middleware = VerifyUserMiddleware()
    response = middleware.process_request(request)
    assert response.url == '%s?next=/admin/' % reverse('wagtail_2fa_auth')


def test_superuser_require_register_device(rf, superuser):
    request = rf.get('/admin/')
    request.user = superuser

    middleware = VerifyUserMiddleware()
    response = middleware.process_request(request)
    assert response.url == '%s?next=/admin/' % reverse('wagtail_2fa_device_list')
