from django import forms

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
