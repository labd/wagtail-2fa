from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice


def get_or_create_unconfirmed_device(user):
    """Return the user's pending device, creating one only if there is none."""
    device = TOTPDevice.objects.devices_for_user(user, confirmed=False).first()

    if device is None:
        num = TOTPDevice.objects.filter(user=user).count()
        device = TOTPDevice.objects.create(
            name=_("Device #%s") % (num + 1), user=user, confirmed=False
        )

    return device


def delete_unconfirmed_devices(user):
    (TOTPDevice.objects.devices_for_user(user, confirmed=False).delete())
