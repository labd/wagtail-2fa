from django.urls import path, reverse
from wagtail.core import hooks

from wagtail_2fa import views
from wagtail.admin.menu import MenuItem


@hooks.register('register_admin_urls')
def urlpatterns():
    return [
        path('2fa/auth', views.LoginView.as_view(), name='wagtail_2fa_auth'),
        path('2fa/devices/', views.DeviceListView.as_view(), name='wagtail_2fa_device_list'),
        path('2fa/devices/new', views.DeviceCreateView.as_view(), name='wagtail_2fa_device_new'),
        path('2fa/devices/remove/<int:pk>', views.DeviceDeleteView.as_view(), name='wagtail_2fa_device_remove'),
        path('2fa/devices/qr-code', views.DeviceQRCodeView.as_view(), name='wagtail_2fa_device_qrcode'),
    ]


@hooks.register('construct_main_menu')
def remove_menu_if_unverified(request, menu_items):
    if not request.user.is_verified():
        menu_items.clear()
        menu_items.append(
            MenuItem('2FA Setup', reverse('wagtail_2fa_device_list'))
        )
