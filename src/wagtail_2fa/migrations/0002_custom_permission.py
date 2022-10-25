from django.db import migrations


def create_2fa_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')

    wagtail_2fa_content_type, created = ContentType.objects.get_or_create(
        app_label='wagtail_2fa',
        model='admin'
    )

    # Create 2FA permission
    enable_2fa_permission, created = Permission.objects.get_or_create(
        content_type=wagtail_2fa_content_type,
        codename='enable_2fa',
        name='Enable 2FA'
    )


def remove_2fa_permissions(apps, schema_editor):
    """Reverse the above additions of permissions."""
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    wagtail_2fa_content_type = ContentType.objects.get(
        app_label='wagtail_2fa',
        model='admin',
    )

    # This also removes the permission from all groups
    Permission.objects.filter(
        content_type=wagtail_2fa_content_type,
        codename='enable_2fa',
    ).delete()


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(create_2fa_permissions, remove_2fa_permissions),
    ]
