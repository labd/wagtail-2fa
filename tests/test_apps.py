import pytest
from django.apps import apps

from wagtail_2fa.apps import WAGTAIL_2FA_DEFAULT_SETTINGS


@pytest.mark.parametrize("setting_name,expected_value", [
    ('WAGTAIL_2FA_REQUIRED', False),
    ('WAGTAIL_2FA_OTP_TOTP_NAME', False),
])
def test_setting_default_values(setting_name, expected_value, settings):
    # Explicitly deleting settings to ensure it's added when ready() is called
    delattr(settings, setting_name)

    app_config = apps.get_app_config('wagtail_2fa')
    app_config.ready()

    assert getattr(settings, setting_name) == expected_value


@pytest.mark.parametrize("setting_name", [
    'WAGTAIL_2FA_OTP_TOTP_NAME',
    'WAGTAIL_SITE_NAME',
    'OTP_TOTP_ISSUER'
])
def test_otp_totp_issuer(setting_name, settings):
    setattr(settings, setting_name, 'wagtail-2fa')

    app_config = apps.get_app_config('wagtail_2fa')
    app_config.ready()

    assert settings.OTP_TOTP_ISSUER == 'wagtail-2fa'
