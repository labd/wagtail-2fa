from django.conf import settings
from django.contrib.auth.models import Permission
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from wagtail import hooks, VERSION as WAGTAIL_VERSION
from wagtail.admin.menu import MenuItem
from wagtail.users.widgets import UserListingButton


from wagtail_2fa import views


@hooks.register("register_admin_urls")
def urlpatterns():
    return [
        path("2fa/auth", views.LoginView.as_view(), name="wagtail_2fa_auth"),
        path(
            "2fa/devices/<int:user_id>",
            views.DeviceListView.as_view(),
            name="wagtail_2fa_device_list",
        ),
        path(
            "2fa/devices/new",
            views.DeviceCreateView.as_view(),
            name="wagtail_2fa_device_new",
        ),
        path(
            "2fa/devices/<int:pk>/update",
            views.DeviceUpdateView.as_view(),
            name="wagtail_2fa_device_update",
        ),
        path(
            "2fa/devices/<int:pk>/remove",
            views.DeviceDeleteView.as_view(),
            name="wagtail_2fa_device_remove",
        ),
        path(
            "2fa/devices/qr-code",
            views.DeviceQRCodeView.as_view(),
            name="wagtail_2fa_device_qrcode",
        ),
    ]


@hooks.register("construct_main_menu")
def remove_menu_if_unverified(request, menu_items):
    """Remove the sidebar menu items if the user is unverified."""
    if (
        settings.WAGTAIL_2FA_REQUIRED
        and getattr(request.user, "enable_2fa", True)
        and not request.user.is_verified()
    ):
        menu_items.clear()
        menu_items.append(
            MenuItem(
                "2FA Setup",
                reverse("wagtail_2fa_device_list", kwargs={"user_id": request.user.id}),
            )
        )


@hooks.register("register_account_menu_item")
def register(request):
    return {
        "url": reverse("wagtail_2fa_device_list", kwargs={"user_id": request.user.id}),
        "label": _("Manage your 2FA devices"),
        "help_text": _("Add or remove devices for 2 factor authentication."),
    }


if WAGTAIL_VERSION >= (6, 1):
    @hooks.register("register_user_listing_buttons")
    def register_user_listing_buttons(user, request_user):
        yield UserListingButton(
            _("Manage 2FA"),
            reverse("wagtail_2fa_device_list", kwargs={"user_id": user.id}),
            attrs={"title": _("Edit this user")},
            priority=100,
        )
else:
    @hooks.register("register_user_listing_buttons")
    def register_user_listing_buttons(context, user):
        yield UserListingButton(
            _("Manage 2FA"),
            reverse("wagtail_2fa_device_list", kwargs={"user_id": user.id}),
            attrs={"title": _("Edit this user")},
            priority=100,
        )


@hooks.register("register_permissions")
def register_2fa_permission():
    if "wagtail_2fa.middleware.VerifyUserPermissionsMiddleware" in settings.MIDDLEWARE:
        return Permission.objects.filter(
            content_type__app_label="wagtailadmin", codename="enable_2fa"
        )

    return Permission.objects.none()
