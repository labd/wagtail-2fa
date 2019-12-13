from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice

from wagtail_2fa import forms


def get_unconfirmed_device(user):
    return TOTPDevice.objects.devices_for_user(user, confirmed=False).first()


def new_unconfirmed_device(user):
    delete_unconfirmed_devices(user)
    num = TOTPDevice.objects.filter(user=user).count()
    return TOTPDevice.objects.create(
        name=_("Device #%s") % (num + 1), user=user, confirmed=False
    )


def delete_unconfirmed_devices(user):
    (TOTPDevice.objects.devices_for_user(user, confirmed=False).delete())


def get_device_form():
    return forms.DeviceForm if (
        settings.WAGTAIL_CHECK_PASSWORD_IN_DEVICE_FORM
    ) else forms.DeviceFormNoPassword
