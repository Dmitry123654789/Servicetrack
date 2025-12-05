__all__ = ()

import django.contrib.auth.forms
import django.forms
from django.utils.translation import gettext_lazy as _
import phonenumber_field.formfields

import users.models


class CustomUserCreationForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        label=_("Электронная_почта"),
        max_length=254,
        widget=django.forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    phone = phonenumber_field.formfields.PhoneNumberField(
        label=_("Телефон"),
        required=False,
        region="RU",
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.CustomUser
        fields = ("username", "email", "phone", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Имя_пользователя")
        self.fields["password1"].label = _("Пароль")
        self.fields["password2"].label = _("Подтверждение_пароля")


class CustomAuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    username = django.forms.CharField(
        label=_("Имя_пользователя"),
        widget=django.forms.TextInput(attrs={"autofocus": True}),
    )
    password = django.forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "current-password"},
        ),
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста,_введите_правильные имя_пользователя_и_пароль."
            "Оба_поля_могут_быть_чувствительны_к_регистру.",
        ),
        "inactive": _("Этот_аккаунт_неактивен"),
    }


class CustomPasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    old_password = django.forms.CharField(
        label=_("Старый_пароль"),
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True},
        ),
    )
    new_password1 = django.forms.CharField(
        label=_("Новый_пароль"),
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "new-password"},
        ),
        strip=False,
    )
    new_password2 = django.forms.CharField(
        label=_("Подтверждение_нового_пароля"),
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "new-password"},
        ),
    )


class CustomPasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    email = django.forms.EmailField(
        label=_("Электронная_почта"),
        max_length=254,
        widget=django.forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class CustomSetPasswordForm(django.contrib.auth.forms.SetPasswordForm):
    new_password1 = django.forms.CharField(
        label=_("Новый_пароль"),
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "new-password"},
        ),
        strip=False,
    )
    new_password2 = django.forms.CharField(
        label=_("Подтверждение_нового_пароля"),
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={"autocomplete": "new-password"},
        ),
    )
