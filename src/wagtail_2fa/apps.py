
from django.conf import settings
from django.apps import AppConfig


class Wagtail2faConfig(AppConfig):
    name = 'wagtail_2fa'
    label = 'wagtail_2fa'
    verbose_name = "Wagtail 2FA"

    def ready(self):
        if not hasattr(settings, 'WAGTAIL_2FA_REQUIRED'):
            settings.WAGTAIL_2FA_REQUIRED = False
