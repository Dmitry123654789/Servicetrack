__all__ = ()

import django.contrib.admin

import tickets.models


@django.contrib.admin.register(tickets.models.Ticket)
class WorkerGroupAdmin(django.contrib.admin.ModelAdmin):
    model = tickets.models.Ticket
