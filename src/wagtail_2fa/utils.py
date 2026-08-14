from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice


def user_can_manage_other_users_devices(user):
    """
    Whether `user` may create, view, or delete 2FA devices belonging to other users.

    Checks the narrow, package-owned `manage_2fa_devices` permission first
    (configurable via WAGTAIL_2FA_MANAGE_DEVICES_PERMISSION), then falls
    back to the consuming project's own change_user permission.
    """
    permission = getattr(
        settings,
        "WAGTAIL_2FA_MANAGE_DEVICES_PERMISSION",
        "wagtailadmin.manage_2fa_devices",
    )
    if permission and user.has_perm(permission):
        return True

    User = get_user_model()
    return user.has_perm(f"{User._meta.app_label}.change_{User._meta.model_name}")


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
