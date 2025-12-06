__all__ = ()

import django.conf
import django.db.models
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import tickets.utils
import users.models


class TicketQuerySet(django.db.models.QuerySet):
    def with_priority_weight(self):
        return self.annotate(
            priority_weight=django.db.models.Case(
                django.db.models.When(
                    priority="low", then=django.db.models.Value(1),
                ),
                django.db.models.When(
                    priority="medium", then=django.db.models.Value(2),
                ),
                django.db.models.When(
                    priority="high", then=django.db.models.Value(3),
                ),
                django.db.models.When(
                    priority="critical", then=django.db.models.Value(4),
                ),
                default=django.db.models.Value(5),
                output_field=django.db.models.IntegerField(),
            ),
        )

    def with_status_weight(self):
        return self.annotate(
            status_weight=django.db.models.Case(
                django.db.models.When(
                    status="open", then=django.db.models.Value(1),
                ),
                django.db.models.When(
                    status="in_progress", then=django.db.models.Value(2),
                ),
                django.db.models.When(
                    status="closed", then=django.db.models.Value(3),
                ),
                django.db.models.When(
                    status="cancelled", then=django.db.models.Value(4),
                ),
                default=django.db.models.Value(5),
                output_field=django.db.models.IntegerField(),
            ),
        )

    def sort(
        self,
        status=None,
        priority=None,
        created=None,
    ):
        # "asc"(возростание) или "desc"(убывание) или None

        ordering = []

        if status:
            sign = "" if status == "asc" else "-"
            ordering.append(f"{sign}status_weight")

        if priority:
            sign = "" if priority == "asc" else "-"
            ordering.append(f"{sign}priority_weight")

        if created:
            sign = "" if created == "asc" else "-"
            ordering.append(f"{sign}created_at")

        if ordering:
            print(*ordering)
            return self.order_by(*ordering)

        return self


class TicketManager(django.db.models.Manager):
    def get_queryset(self):
        return TicketQuerySet(self.model, using=self._db)

    def get_list(self):
        queryset = (
            self.get_queryset()
            .select_related(
                Ticket.assignee.field.name,
            )
        )

        return (
            queryset.only(
                Ticket.title.field.name,
                Ticket.status.field.name,
                Ticket.priority.field.name,
                Ticket.created_at.field.name,
                f"{Ticket.assignee.field.name}_"
                f"_{users.models.CustomUser.username.field.name}",
            )
        )


class Ticket(django.db.models.Model):
    objects = TicketManager()

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


class StatusLog(django.db.models.Model):
    ticket = django.db.models.ForeignKey(
        Ticket,
        verbose_name=_("заявка"),
        on_delete=django.db.models.CASCADE,
        related_name="status_logs",
    )

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name=_("пользователь"),
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        related_name="status_changes",
    )

    from_status = django.db.models.CharField(
        _("из_статуса"),
        choices=Ticket.Status.choices,
    )

    to_status = django.db.models.CharField(
        _("в_статус"),
        choices=Ticket.Status.choices,
    )

    timestamp = django.db.models.DateTimeField(
        _("время_изменения"),
        auto_now_add=True,
    )

    comment = django.db.models.TextField(
        _("комментарий"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("история_изменения_статуса")
        verbose_name_plural = _("истории_изменений_статусов")

    def __str__(self):
        return self.ticket.title
