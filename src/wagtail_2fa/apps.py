from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

WAGTAIL_2FA_DEFAULT_SETTINGS = {
    "WAGTAIL_2FA_REQUIRED": False,
    "WAGTAIL_2FA_OTP_TOTP_NAME": False,
    "WAGTAIL_MOUNT_PATH": "",
}


class Wagtail2faConfig(AppConfig):
    name = "wagtail_2fa"
    label = "wagtail_2fa"
    verbose_name = "Wagtail 2FA"

    def ready(self):
        if "wagtail_2fa.middleware.VerifyUserMiddleware" not in settings.MIDDLEWARE:
            raise ImproperlyConfigured(
                "Please add 'wagtail_2fa.middleware.VerifyUserMiddleware' "
                "to django.conf.settings.MIDDLEWARE"
            )

        for setting_name, setting_default_value in WAGTAIL_2FA_DEFAULT_SETTINGS.items():
            if not hasattr(settings, setting_name):
                setattr(settings, setting_name, setting_default_value)

        # Set OTP_TOTP_ISSUER, to identify the app, in authenticator
        # only set this if it's not already set
        if not hasattr(settings, "OTP_TOTP_ISSUER"):
            if not settings.WAGTAIL_2FA_OTP_TOTP_NAME and hasattr(
                settings, "WAGTAIL_SITE_NAME"
            ):
                settings.OTP_TOTP_ISSUER = settings.WAGTAIL_SITE_NAME
            elif settings.WAGTAIL_2FA_OTP_TOTP_NAME:
                settings.OTP_TOTP_ISSUER = settings.WAGTAIL_2FA_OTP_TOTP_NAME
