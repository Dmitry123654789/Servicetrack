__all__ = ()

import django.contrib.admin
import django.utils.safestring
from django.utils.translation import gettext_lazy as _

import tickets.models


@django.contrib.admin.register(tickets.models.Ticket)
class TicketAdmin(django.contrib.admin.ModelAdmin):
    model = tickets.models.Ticket

    def show_photo_before(self, obj):
        return django.utils.safestring.mark_safe(
            f'<img src="{obj.url_photo_before()}"'
            'width="400" height="300" class="img-fluid rounded shadow-sm">',
        )

    show_photo_before.short_description = _("фото")

    def show_photo_after(self, obj):
        return django.utils.safestring.mark_safe(
            f'<img src="{obj.url_photo_after()}"'
            'width="400" height="300" class="img-fluid rounded shadow-sm">',
        )

    show_photo_after.short_description = _("фото")

    fields = (
        model.title.field.name,
        model.description.field.name,
        model.status.field.name,
        model.priority.field.name,
        model.group.field.name,
        model.creator.field.name,
        model.assignee.field.name,
        (
            model.photo_before.field.name,
            show_photo_before.__name__,
        ),
        (
            model.photo_after.field.name,
            show_photo_after.__name__,
        ),
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    readonly_fields = (
        show_photo_before.__name__,
        show_photo_after.__name__,
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    list_display = (
        model.title.field.name,
        model.status.field.name,
        model.priority.field.name,
        model.group.field.name,
    )


@django.contrib.admin.register(tickets.models.StatusLog)
class TicketStatusLogAdmin(django.contrib.admin.ModelAdmin):
    model = tickets.models.StatusLog
    can_delete = False

    fields = (
        model.ticket.field.name,
        model.user.field.name,
        model.from_status.field.name,
        model.to_status.field.name,
        model.timestamp.field.name,
        model.comment.field.name,
    )

    readonly_fields = (
        model.ticket.field.name,
        model.user.field.name,
        model.from_status.field.name,
        model.to_status.field.name,
        model.timestamp.field.name,
        model.comment.field.name,
    )

    list_display = (
        model.ticket.field.name,
        model.from_status.field.name,
        model.to_status.field.name,
        model.timestamp.field.name,
    )
