__all__ = ()

import django.forms

import company.models
import users.models


class OrganizationForm(django.forms.ModelForm):
    class Meta:
        model = company.models.Organization
        fields = (
            "name",
            "description",
        )


class WorkerGroupEditForm(django.forms.ModelForm):
    class Meta:
        model = company.models.WorkerGroup
        fields = (
            "name",
            "description",
            "manager",
            "workers",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        organization = self.request.user.profile.organization

        self.fields["manager"].queryset = (
            users.models.CustomUser.objects.filter(
                profile__organization=organization,
                profile__role=users.models.Profile.Role.GROUP_MANAGER,
            )
        )

        self.fields["workers"].queryset = (
            users.models.CustomUser.objects.filter(
                profile__organization=organization,
                profile__role=users.models.Profile.Role.WORKER,
            )
        )

        self.fields["workers"].widget = django.forms.CheckboxSelectMultiple()

        if not self.request.user.profile.is_director:
            self.fields["manager"].disabled = True
            self.fields["manager"].readonly = True


class WorkerGroupCreationForm(django.forms.ModelForm):
    class Meta:
        model = company.models.WorkerGroup
        fields = (
            "name",
            "description",
            "manager",
            "workers",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        organization = self.request.user.profile.organization

        self.fields["manager"].queryset = (
            users.models.CustomUser.objects.filter(
                profile__organization=organization,
                profile__role=users.models.Profile.Role.GROUP_MANAGER,
            )
        )

        self.fields["workers"].queryset = (
            users.models.CustomUser.objects.filter(
                profile__organization=organization,
                profile__role=users.models.Profile.Role.WORKER,
            )
        )

        self.fields["workers"].widget = django.forms.CheckboxSelectMultiple()
