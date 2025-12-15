__all__ = ()

import django.conf
import django.db.models
from django.utils.translation import gettext_lazy as _

import users.models


class Organization(django.db.models.Model):
    name = django.db.models.CharField(
        _("название_организации"),
        max_length=255,
    )

    description = django.db.models.TextField(
        _("описание"),
        blank=True,
        null=True,
    )

    main_manager = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="organization",
        verbose_name=_("управляющий_организацией"),
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
        verbose_name = _("организация")
        verbose_name_plural = _("организации")

    def __str__(self):
        return self.name


class WorkerGroup(django.db.models.Model):
    name = django.db.models.CharField(
        _("название_группы"),
        max_length=100,
    )

    description = django.db.models.TextField(
        _("описание"),
        blank=True,
        null=True,
    )

    workers = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("работники"),
        related_name="work_groups",
        blank=True,
        limit_choices_to={"profile__role": users.models.Profile.Role.WORKER},
    )

    manager = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("руководитель_группы"),
        related_name="managed_groups",
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={
            "profile__role": users.models.Profile.Role.GROUP_MANAGER,
        },
    )

    organization = django.db.models.ForeignKey(
        Organization,
        on_delete=django.db.models.CASCADE,
        related_name="groups",
        verbose_name=_("организация"),
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
