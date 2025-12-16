__all__ = ()

import django.contrib.auth
import django.db.models
import django.forms
from django.utils.translation import gettext_lazy as _

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

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        user_organization = current_user.profile.organization
        self.fields["group"].queryset = self.fields["group"].queryset.filter(
            organization=user_organization,
            workers=current_user,
        )

        self.fields["status"].disabled = True


class TicketWorkerForm(django.forms.ModelForm):
    transitions = {
        tickets.models.Ticket.Status.OPEN: [
            tickets.models.Ticket.Status.IN_PROGRESS,
            tickets.models.Ticket.Status.CANCELLED,
        ],
        tickets.models.Ticket.Status.IN_PROGRESS: [
            tickets.models.Ticket.Status.CLOSED,
            tickets.models.Ticket.Status.CANCELLED,
        ],
        tickets.models.Ticket.Status.CLOSED: [],
        tickets.models.Ticket.Status.CANCELLED: [],
    }

    comment = django.forms.CharField(
        label="Комментарий",
        required=False,
        widget=django.forms.Textarea(),
    )

    class Meta:
        model = tickets.models.Ticket
        fields = (
            tickets.models.Ticket.title.field.name,
            tickets.models.Ticket.description.field.name,
            tickets.models.Ticket.status.field.name,
            tickets.models.Ticket.photo_after.field.name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        readonly = (
            tickets.models.Ticket.title.field.name,
            tickets.models.Ticket.description.field.name,
        )

        for field in readonly:
            self.fields[field].disabled = True

        self.fields["status"].choices = self._get_allowed_status()

    def clean_status(self):
        new_status = self.cleaned_data.get("status")

        if not self.instance or new_status == self.instance.status:
            return new_status

        old_status = self.instance.status
        if new_status not in self.transitions.get(old_status, None):
            error_message = _("Недопустимый_переход_статуса.")
            raise django.forms.ValidationError(error_message)

        return new_status

    def _get_allowed_status(self):
        old_status = self.instance.status
        allowed_statuses = self.transitions.get(
            old_status, None,
        )

        choices = [(old_status, self.instance.get_status_display())]
        all_choices = tickets.models.Ticket.Status.choices

        choices += [
            choice for choice in all_choices if choice[0] in allowed_statuses
        ]
        return choices


class TicketManagerForm(django.forms.ModelForm):
    comment = django.forms.CharField(
        label="Комментарий",
        required=False,
        widget=django.forms.Textarea(),
    )

    class Meta:
        model = tickets.models.Ticket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["creator"].disabled = True

        user_organization = current_user.profile.organization
        self.fields["group"].queryset = self.fields["group"].queryset.filter(
            organization=user_organization,
        )

        if self.instance and self.instance.pk:
            group = self.instance.group
            user_model = django.contrib.auth.get_user_model()

            self.fields["assignee"].queryset = user_model.objects.filter(
                django.db.models.Q(work_groups=group)
                | django.db.models.Q(pk=group.manager_id),
            )

            if not current_user.profile.is_director:
                self.fields["group"].disabled = True
