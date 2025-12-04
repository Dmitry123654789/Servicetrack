__all__ = ()

import django.contrib.auth.models as auth_models
import django.db.models
from django.utils.translation import gettext_lazy as _
import phonenumber_field.modelfields


class CustomUser(auth_models.AbstractUser):
    email = django.db.models.EmailField(
        verbose_name=_("электронная_почта"),
        unique=True,
    )

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ["email"]


class Profile(django.db.models.Model):
    class Role(django.db.models.TextChoices):
        MAIN_MANAGER = "main_manager", _("директор")
        GROUP_MANAGER = "group_manager", _("руководитель_группы")
        WORKER = "worker", _("работник")

    user = django.db.models.OneToOneField(
        CustomUser,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
        verbose_name=_("пользователь"),
    )

    role = django.db.models.CharField(
        _("роль"),
        choices=Role.choices,
        default=Role.WORKER,
    )

    phone = phonenumber_field.modelfields.PhoneNumberField(
        _("телефон"),
        blank=True,
        null=True,
        region="RU",
    )

    class Meta:
        verbose_name = _("данные_пользователя")
        verbose_name_plural = _("данные_пользователей")

    def __str__(self):
        return self.user.username


class WorkerGroup(django.db.models.Model):
    name = django.db.models.CharField(
        _("название_группы"),
        max_length=100,
        unique=True,
    )

    description = django.db.models.TextField(
        _("описание"),
        blank=True,
        null=True,
    )

    workers = django.db.models.ManyToManyField(
        CustomUser,
        verbose_name=_("работники"),
        related_name="work_groups",
        blank=True,
        limit_choices_to={"profile__role": Profile.Role.WORKER},
    )

    manager = django.db.models.ForeignKey(
        CustomUser,
        verbose_name=_("руководитель_группы"),
        related_name="managed_groups",
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"profile__role": Profile.Role.GROUP_MANAGER},
    )

    created_at = django.db.models.DateTimeField(
        _("дата_создания"),
        auto_now_add=True,
    )

    updated_at = django.db.models.DateTimeField(
        _("дата_обновления"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("рабочая_группа")
        verbose_name_plural = _("рабочие_группы")

    def __str__(self):
        return self.name
