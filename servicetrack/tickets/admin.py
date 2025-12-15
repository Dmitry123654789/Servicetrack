__all__ = ()

import django.contrib.admin

import tickets.models


@django.contrib.admin.register(tickets.models.Ticket)
class TicketAdmin(django.contrib.admin.ModelAdmin):
    model = tickets.models.Ticket

    fields = (
        model.title.field.name,
        model.description.field.name,
        model.status.field.name,
        model.priority.field.name,
        model.group.field.name,
        model.creator.field.name,
        model.assignee.field.name,
        model.photo_before.field.name,
        model.photo_after.field.name,
        # model.show_photo_before,
        # model.show_photo_after,
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    readonly_fields = (
        # model.show_photo_before,
        # model.show_photo_after,
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
