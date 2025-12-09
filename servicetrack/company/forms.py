__all__ = ()

import django.forms

import company.models


class OrganizationForm(django.forms.ModelForm):
    class Meta:
        model = company.models.Organization
        fields = (
            "name",
            "description",
        )


class WorkerGroupForm(django.forms.ModelForm):
    class Meta:
        model = company.models.WorkerGroup
        fields = (
            "name",
            "description",
            "manager",
            "workers",
        )
