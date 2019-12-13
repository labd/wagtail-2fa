from wagtail_2fa.wagtail_hooks import remove_menu_if_unverified
from django.test import override_settings
from wagtail.admin.menu import MenuItem
from django_otp.middleware import OTPMiddleware as _OTPMiddleware
from django_otp import user_has_device


class TestHooks:
    def test_remove_menu_if_unverified(self, user, rf):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            request = rf.get('/cms/')
            request.user = user
            middleware = _OTPMiddleware()
            user = middleware._verify_user(request, user)
            assert not user_has_device(user)
            assert user.is_authenticated

            menu_items = [
                MenuItem("Dummy item 1", "/stub1/"),
                MenuItem("Dummy item 2", "/stub2/"),
                MenuItem("Dummy item 3", "/stub3/")
            ]

            remove_menu_if_unverified(request, menu_items)

            assert len(menu_items) == 1
            assert menu_items[0].label == "2FA Setup"
            assert menu_items[0].url == "/cms/2fa/devices/1"

    def test_do_not_remove_menu_if_verified(self, verified_user, rf):
        with override_settings(WAGTAIL_2FA_REQUIRED=True):
            request = rf.get('/cms/')
            request.user = verified_user

            menu_items = [
                MenuItem("Dummy item 1", "/stub1/"),
                MenuItem("Dummy item 2", "/stub2/"),
                MenuItem("Dummy item 3", "/stub3/")
            ]

            remove_menu_if_unverified(request, menu_items)

            assert menu_items == menu_items

    def test_do_not_remove_menu_if_2fa_required_is_false(
            self, user, rf):
        with override_settings(WAGTAIL_2FA_REQUIRED=False):
            request = rf.get('/cms/')

            # Use a regular user here to make sure the menu still works
            # even when the middleware is not loaded and the user does not have the
            # enable_2fa permission.
            request.user = user
            assert getattr(request.user, "enable_2fa", None) is None

            menu_items = [
                MenuItem("Dummy item 1", "/stub1/"),
                MenuItem("Dummy item 2", "/stub2/"),
                MenuItem("Dummy item 3", "/stub3/")
            ]

            remove_menu_if_unverified(request, menu_items)

            assert menu_items == menu_items

    def test_do_not_remove_menu_if_2fa_required_is_false_for_verified_user(
            self, verified_user, rf):
        with override_settings(WAGTAIL_2FA_REQUIRED=False):
            request = rf.get('/cms/')
            request.user = verified_user

            menu_items = [
                MenuItem("Dummy item 1", "/stub1/"),
                MenuItem("Dummy item 2", "/stub2/"),
                MenuItem("Dummy item 3", "/stub3/")
            ]

            remove_menu_if_unverified(request, menu_items)

            assert menu_items == menu_items
