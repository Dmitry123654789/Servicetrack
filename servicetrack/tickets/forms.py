__all__ = ()

import django.forms

import tickets.models


class TicketCreateForm(django.forms.ModelForm):
    class Meta:
        model = tickets.models.Ticket
        fields = [
            tickets.models.Ticket.title.field.name,
            tickets.models.Ticket.description.field.name,
            tickets.models.Ticket.status.field.name,
            tickets.models.Ticket.priority.field.name,
            tickets.models.Ticket.group.field.name,
            tickets.models.Ticket.photo_before.field.name,
        ]


class TicketWorkerForm(django.forms.ModelForm):
    comment = django.forms.CharField(
        label="Комментарий",
        required=False,
        widget=django.forms.Textarea(),
    )

    class Meta:
        model = tickets.models.Ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        readonly = [
            tickets.models.Ticket.title.field.name,
            tickets.models.Ticket.description.field.name,
            tickets.models.Ticket.group.field.name,
            tickets.models.Ticket.creator.field.name,
            tickets.models.Ticket.assignee.field.name,
            tickets.models.Ticket.photo_before.field.name,
        ]

        for field in readonly:
            self.fields[field].disabled = True
            self.fields[field].readonly = True


class TicketManagerForm(django.forms.ModelForm):
    comment = django.forms.CharField(
        label="Комментарий",
        required=False,
        widget=django.forms.Textarea(),
    )

    class Meta:
        model = tickets.models.Ticket
        fields = "__all__"
