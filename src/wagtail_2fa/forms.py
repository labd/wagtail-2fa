from django import forms
from django.utils.translation import ugettext_lazy as _

from django_otp.forms import OTPAuthenticationFormMixin


class TokenForm(OTPAuthenticationFormMixin, forms.Form):
    otp_token = forms.CharField(required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        self.fields['otp_token'].widget.attrs.update({
            'autofocus': 'autofocus',
            'autocomplete': 'off',
        })

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data


class DeviceForm(forms.Form):
    otp_token = forms.CharField(required=True)

    def __init__(self, user, device, **kwargs):
        super().__init__(**kwargs)
        self.fields['otp_token'].widget.attrs.update({
            'autofocus': 'autofocus',
            'autocomplete': 'off',
        })

        self.user = user
        self.device = device

    def clean_otp_token(self):
        token = self.cleaned_data.get('otp_token')

        if token and self.device.verify_token(token):
            return token

        raise forms.ValidationError(
            _('Invalid token. Please make sure you have entered it correctly.'),
            code='invalid')
