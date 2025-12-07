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
    first_name = django.forms.CharField(
        label=_("Имя"),
        required=False,
        max_length=150,
    )
    last_name = django.forms.CharField(
        label=_("Фамилия"),
        required=False,
        max_length=150,
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Имя_пользователя")
        self.fields["password1"].label = _("Пароль")
        self.fields["password2"].label = _("Подтверждение_пароля")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")

        if commit:
            user.save()
            if self.cleaned_data.get("phone"):
                user.profile.phone = self.cleaned_data["phone"]
                user.profile.save()

        return user


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


class UserCreateForm(django.forms.ModelForm):
    password1 = django.forms.CharField(
        label=_("Пароль"),
        widget=django.forms.PasswordInput,
    )
    password2 = django.forms.CharField(
        label=_("Подтверждение пароля"),
        widget=django.forms.PasswordInput,
    )

    class Meta:
        model = users.models.CustomUser
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("creator", None)
        super().__init__(*args, **kwargs)

        if (
            self.creator
            and self.creator.profile.role
            == users.models.Profile.Role.MAIN_MANAGER
        ):
            self.fields["role"] = django.forms.ChoiceField(
                label=_("Роль"),
                choices=[
                    (
                        users.models.Profile.Role.GROUP_MANAGER,
                        _("Руководитель группы"),
                    ),
                    (users.models.Profile.Role.WORKER, _("Работник")),
                ],
                initial=users.models.Profile.Role.WORKER,
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise django.forms.ValidationError(_("Пароли не совпадают"))

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            profile, created = users.models.Profile.objects.get_or_create(
                user=user,
                defaults={"role": users.models.Profile.Role.WORKER},
            )
            if "role" in self.cleaned_data:
                profile.role = self.cleaned_data.get("role")
                profile.save()

        return user


class UserProfileUpdateForm(django.forms.ModelForm):
    phone = phonenumber_field.formfields.PhoneNumberField(
        label=_("Телефон"),
        required=False,
        region="RU",
    )

    class Meta:
        model = users.models.CustomUser
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "profile"):
            self.fields["phone"].initial = self.instance.profile.phone

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            if hasattr(user, "profile"):
                user.profile.phone = self.cleaned_data.get("phone")
                user.profile.save()

        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            users.models.CustomUser.objects.filter(email=email)  # noqa: ECE001
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise django.forms.ValidationError(
                _("Этот email уже используется другим пользователем"),
            )

        return email
