from django_otp.plugins.otp_totp.models import TOTPDevice


def get_unconfirmed_device(user):
    return(
        TOTPDevice.objects
        .devices_for_user(user, confirmed=False)
        .first())


def new_unconfirmed_device(user):
    delete_unconfirmed_devices(user)
    return TOTPDevice.objects.create(user=user, confirmed=False)


def delete_unconfirmed_devices(user):
    (TOTPDevice.objects
        .devices_for_user(user, confirmed=False)
        .delete())
