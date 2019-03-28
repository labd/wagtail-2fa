from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import get_user_model

def test_device_list_view(admin_client):
    response = admin_client.get(reverse('wagtail_2fa_device_list'))
    assert response.status_code == 200


def test_device_list_create(admin_client, monkeypatch):
    response = admin_client.get(reverse('wagtail_2fa_device_new'))
    assert response.status_code == 200

    def verify_token(self, value):
        return value == '123456'

    monkeypatch.setattr(TOTPDevice, 'verify_token', verify_token)

    response = admin_client.post(
        reverse('wagtail_2fa_device_new'), {
            'name': 'Test device',
            'otp_token': '123456',
            'password': 'password',
        })

    assert response.status_code == 302, response.context['form'].errors
    assert TOTPDevice.objects.filter(confirmed=True).count() == 1


def test_device_list_update(admin_client, monkeypatch):
    user = get_user_model().objects.filter(is_staff=True).first()
    instance = TOTPDevice.objects.create(name='Initial', user=user, confirmed=True)

    monkeypatch.setattr(TOTPDevice, 'verify_token', lambda self, value: True)

    # Login with 2fa
    endpoint = reverse('wagtail_2fa_auth')
    response = admin_client.post(endpoint, {'otp_token': '123456', 'next': '/cms/'})
    assert response.status_code == 302,  response.context['form'].errors

    # Get update view
    endpoint = reverse('wagtail_2fa_device_update', kwargs={'pk': instance.pk})
    response = admin_client.get(endpoint)
    assert response.status_code == 200

    # Post new name
    response = admin_client.post(endpoint, {
        'name': 'Test device',
        'password': 'password',
    })
    assert response.status_code == 302, response.context['form'].errors
    assert TOTPDevice.objects.filter(name='Test device').count() == 1


def test_device_qr(admin_client, monkeypatch):
    user = get_user_model().objects.filter(is_staff=True).first()
    TOTPDevice.objects.create(name='Initial', user=user, confirmed=False)

    # Get update view
    endpoint = reverse('wagtail_2fa_device_qrcode')
    response = admin_client.get(endpoint)
    assert response.status_code == 200
