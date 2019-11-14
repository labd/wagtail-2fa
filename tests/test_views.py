from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice


def test_device_list_view(admin_client):
    user = get_user_model().objects.filter(is_staff=True).first()
    response = admin_client.get(reverse('wagtail_2fa_device_list', kwargs={'user_id': user.id}))
    assert response.status_code == 200


def test_device_list_create(admin_client, monkeypatch):
    response = admin_client.get(reverse('wagtail_2fa_device_new'))
    assert response.status_code == 200

    with patch("django_otp.plugins.otp_totp.models.TOTPDevice.verify_token") as fn:
        fn.return_value = True
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


def test_delete_user_device_as_admin(admin_client, user, monkeypatch):
    user = get_user_model().objects.filter(is_staff=False).first()
    device = TOTPDevice.objects.create(name='Initial', user=user, confirmed=True)

    endpoint = reverse('wagtail_2fa_device_remove', kwargs={'pk': device.id})
    response = admin_client.post(endpoint, {
        'user_id': user.id
    })
    assert response.status_code == 302
    assert TOTPDevice.objects.all().count() == 0


def test_delete_user_device_unauthorized(client, user, monkeypatch):
    user = get_user_model().objects.filter(is_staff=False).first()
    device = TOTPDevice.objects.create(name='Initial', user=user, confirmed=True)

    endpoint = reverse('wagtail_2fa_device_remove', kwargs={'pk': device.id})
    response = client.post(endpoint, {
        'user_id': user.id
    })
    assert response.status_code == 302
    assert TOTPDevice.objects.all().count() == 1
