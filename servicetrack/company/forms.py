__all__ = ()

import django.contrib.auth
import django.db.models
import django.forms

import company.models
import users.models


class WorkerGroupForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        organization = self.request.user.profile.organization
        user_model = django.contrib.auth.get_user_model()

        self.fields["manager"].queryset = user_model.objects.filter(
            profile__organization=organization,
            profile__role=users.models.Profile.Role.GROUP_MANAGER,
        )

        self.fields["workers"].queryset = user_model.objects.filter(
            profile__organization=organization,
        ).filter(
            django.db.models.Q(
                profile__role=users.models.Profile.Role.WORKER,
            )
            | django.db.models.Q(
                profile__role=users.models.Profile.Role.GROUP_MANAGER,
            ),
        )

        self.fields["workers"].widget = django.forms.CheckboxSelectMultiple()

    def clean_workers(self):
        workers_queryset = self.cleaned_data.get("workers")
        manager = self.cleaned_data.get("manager")

        if workers_queryset and manager and manager in workers_queryset:
            workers_list = list(workers_queryset)
            workers_list.remove(manager)
            return workers_list

        return workers_queryset


class OrganizationForm(WorkerGroupForm):
    class Meta:
        model = company.models.Organization
        fields = (
            model.name.field.name,
            model.description.field.name,
        )


class WorkerGroupEditForm(WorkerGroupForm):
    class Meta:
        model = company.models.WorkerGroup
        fields = (
            model.name.field.name,
            model.description.field.name,
            model.manager.field.name,
            model.workers.field.name,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.request.user.profile.is_director:
            self.fields["manager"].disabled = True


class WorkerGroupCreationForm(WorkerGroupForm):
    class Meta:
        model = company.models.WorkerGroup
        fields = (
            model.name.field.name,
            model.description.field.name,
            model.manager.field.name,
            model.workers.field.name,
        )
