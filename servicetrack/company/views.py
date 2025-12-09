__all__ = ()

import django.views.generic

import company.forms
import company.models


class OrganizationView(django.views.generic.DetailView):
    model = company.models.Organization
    template_name = "company/organization_detail.html"
    context_object_name = "organization"


class OrganizationEditView(django.views.generic.UpdateView):
    model = company.models.Organization
    form_class = company.forms.OrganizationForm
    template_name = "company/organization_edit.html"
    context_object_name = "organization"

    def get_success_url(self):
        print("sdisdi")
        return self.request.path


class GroupEditView(django.views.generic.UpdateView):
    model = company.models.WorkerGroup
    form_class = company.forms.WorkerGroupForm
    template_name = "company/group_edit.html"
    context_object_name = "group"

    def get_success_url(self):
        return self.request.path
