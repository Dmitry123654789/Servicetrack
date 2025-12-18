__all__ = ()

import django.contrib.auth.forms
import django.db
import django.forms
from django.utils.translation import gettext_lazy as _
import phonenumber_field.formfields

import company.models
import users.models


class CustomUserCreationForm(django.contrib.auth.forms.UserCreationForm):
    phone = phonenumber_field.formfields.PhoneNumberField(
        label=_("Телефон"),
        required=False,
        region="RU",
    )

    organization_name = django.forms.CharField(
        label=_("Название организации"),
        max_length=255,
        required=True,
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.CustomUser
        fields = (
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_name.field.name,
            users.models.Profile.phone.field.name,
            "organization_name",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Имя_пользователя")
        self.fields["password1"].label = _("Пароль")
        self.fields["password2"].label = _("Подтверждение_пароля")

    def save(self, commit=True):
        with django.db.transaction.atomic():
            user = super().save(commit=False)
            user.save()

            if commit:
                organization = company.models.Organization.objects.create(
                    name=self.cleaned_data["organization_name"],
                    main_manager=user,
                )

                user.refresh_from_db()
                profile = user.profile

                profile.phone = self.cleaned_data.get("phone", None)
                profile.organization = organization
                profile.role = users.models.Profile.Role.MAIN_MANAGER
                profile.save()

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
        fields = (
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_name.field.name,
        )

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("creator")
        super().__init__(*args, **kwargs)

        choices = [(users.models.Profile.Role.WORKER, _("Работник"))]

        if self.creator.profile.is_director:
            choices.append(
                (
                    users.models.Profile.Role.GROUP_MANAGER,
                    _("Руководитель_группы"),
                ),
            )

        self.fields["role"] = django.forms.ChoiceField(
            label=_("Роль"),
            choices=choices,
            required=True,
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise django.forms.ValidationError(_("Пароли_не_совпадают"))

        return cleaned_data

    def save(self, commit=True):
        with django.db.transaction.atomic():
            creator = self.creator

            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            user.save()

            user.refresh_from_db()
            user.profile.organization_id = creator.profile.organization_id
            user.profile.role = self.cleaned_data["role"]
            user.profile.save()

            if creator.profile.is_manager:
                group = creator.managed_groups.first()
                if group:
                    group.workers.add(user)

            return user


class UserProfileUpdateForm(django.forms.ModelForm):
    phone = phonenumber_field.formfields.PhoneNumberField(
        label=_("Телефон"),
        required=False,
        region="RU",
    )

    class Meta:
        model = users.models.CustomUser
        fields = (
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_name.field.name,
            users.models.Profile.phone.field.name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "profile"):
            self.fields["phone"].initial = self.instance.profile.phone

    def save(self, commit=True):
        with django.db.transaction.atomic():
            user = super().save(commit=False)

            if commit:
                user.save()
                if hasattr(user, "profile"):
                    user.profile.phone = self.cleaned_data.get("phone")
                    user.profile.save()

            return user
