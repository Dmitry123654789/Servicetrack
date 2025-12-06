__all__ = ()

import django.contrib.admin

import tickets.models


@django.contrib.admin.register(tickets.models.Ticket)
class TicketAdmin(django.contrib.admin.ModelAdmin):
    model = tickets.models.Ticket


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
