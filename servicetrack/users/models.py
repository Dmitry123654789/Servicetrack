__all__ = ()

import django.conf
import django.contrib.auth.models as auth_models
import django.db.models
from django.utils.translation import gettext_lazy as _
import phonenumber_field.modelfields


class CustomUser(auth_models.AbstractUser):
    email = django.db.models.EmailField(
        verbose_name=_("почта"),
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
        django.conf.settings.AUTH_USER_MODEL,
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

    organization = django.db.models.ForeignKey(
        "company.Organization",
        verbose_name=_("организация"),
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )

    class Meta:
        verbose_name = _("данные_пользователя")
        verbose_name_plural = _("данные_пользователей")

    def __str__(self):
        return self.user.username

    @property
    def is_director(self):
        return self.role == "main_manager"

    @property
    def is_manager(self):
        return self.role == "group_manager"

    @property
    def is_worker(self):
        return self.role == "worker"
