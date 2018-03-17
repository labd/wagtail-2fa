from django.conf.urls import url
from wagtail.core import hooks

from wagtail_2fa import views


@hooks.register('register_admin_urls')
def urlpatterns():
    return [
        url(r'^otp-auth$', views.LoginView.as_view(), name='wagtail_2fa_auth'),
    ]
