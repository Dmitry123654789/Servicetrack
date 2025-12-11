__all__ = ()

import django.db.models
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

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        user_organization = current_user.profile.organization
        self.fields["group"].queryset = self.fields["group"].queryset.filter(
                organization=user_organization,
                workers=current_user,
            )


class TicketWorkerForm(django.forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["creator"].disabled = True
        self.fields["creator"].readonly = True

        user_organization = current_user.profile.organization
        self.fields["group"].queryset = self.fields["group"].queryset.filter(
                organization=user_organization,
            )

        if self.instance and self.instance.pk:
            group = self.instance.group
            user_model = django.contrib.auth.get_user_model()

            self.fields["assignee"].queryset = user_model.objects.filter(
                django.db.models.Q(work_groups=group) |
                django.db.models.Q(pk=group.manager_id),
            )

            if not current_user.profile.is_director:
                self.fields["group"].disabled = True
