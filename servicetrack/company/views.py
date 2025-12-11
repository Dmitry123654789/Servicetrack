__all__ = ()

from django.contrib.auth.mixins import LoginRequiredMixin
import django.urls
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
        return self.request.path


class GroupListView(LoginRequiredMixin, django.views.generic.ListView):
    model = company.models.WorkerGroup
    template_name = "company/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return company.models.WorkerGroup.objects.filter(
            organization=self.request.user.profile.organization,
        ).select_related("manager")


class GroupDetailView(django.views.generic.DetailView):
    model = company.models.WorkerGroup
    template_name = "company/group_detail.html"
    context_object_name = "group"


class GroupEditView(LoginRequiredMixin, django.views.generic.UpdateView):
    model = company.models.WorkerGroup
    form_class = company.forms.WorkerGroupEditForm
    template_name = "company/group_edit.html"
    context_object_name = "group"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        return self.request.path


class GroupCreateView(LoginRequiredMixin, django.views.generic.CreateView):
    model = company.models.WorkerGroup
    form_class = company.forms.WorkerGroupCreationForm
    template_name = "company/group_create.html"
    success_url = django.urls.reverse_lazy("company:group_list")

    def test_func(self):
        return self.request.user.profile.is_director

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.organization = self.request.user.profile.organization
        return super().form_valid(form)
