from django.apps import apps


def test_sets_default_wagtail_mount_path(settings):
    # WAGTAIL_MOUNT_PATH was already populated in the test environment
    # Explicitly deleting it to ensure it's added when ready() is called
    delattr(settings, 'WAGTAIL_MOUNT_PATH')
    assert not hasattr(settings, 'WAGTAIL_MOUNT_PATH')
    app_config = apps.get_app_config('wagtail_2fa')
    app_config.ready()

    assert settings.WAGTAIL_MOUNT_PATH == ''
