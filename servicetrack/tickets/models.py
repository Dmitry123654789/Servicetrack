__all__ = ()

import django.conf
import django.db.models
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import tickets.utils
import users.models


class Ticket(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        OPEN = "open", _("открыта")
        IN_PROGRESS = "in_progress", _("в_работе")
        CLOSED = "closed", _("закрыта")
        CANCELLED = "cancelled", _("отменена")

    class Priority(django.db.models.TextChoices):
        LOW = "low", _("низкий")
        MEDIUM = "medium", _("средний")
        HIGH = "high", _("высокий")
        CRITICAL = "critical", _("критический")

    title = django.db.models.CharField(
        _("название"),
    )

    description = django.db.models.TextField(
        _("описание"),
    )

    status = django.db.models.CharField(
        _("статус"),
        choices=Status.choices,
        default=Status.OPEN,
    )

    priority = django.db.models.CharField(
        _("приоритет"),
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    group = django.db.models.ForeignKey(
        users.models.WorkerGroup,
        verbose_name=_("рабочая_группа"),
        on_delete=django.db.models.CASCADE,
        related_name="tickets",
    )

    creator = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("создатель"),
        on_delete=django.db.models.CASCADE,
        related_name="created_tickets",
    )

    assignee = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("исполнитель"),
        on_delete=django.db.models.CASCADE,
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )

    photo_before = sorl.thumbnail.ImageField(
        _("фото_до"),
        upload_to=tickets.utils.get_photo_before_path,
        blank=True,
        null=True,
    )

    photo_after = sorl.thumbnail.ImageField(
        _("фото_после"),
        upload_to=tickets.utils.get_photo_after_path,
        blank=True,
        null=True,
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
        verbose_name = _("заявка")
        verbose_name_plural = _("заявки")

    def __str__(self):
        return self.title
