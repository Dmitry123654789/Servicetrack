__all__ = ()

import django.contrib.auth.mixins
import django.db.models
import django.urls
import django.views.generic

import company.forms
import company.models
import core.mixins


class OrganizationView(
    core.mixins.ForbiddenMixin,
    django.views.generic.DetailView,
):
    model = company.models.Organization
    template_name = "company/organization_detail.html"
    context_object_name = "organization"

    def test_func(self):
        organization = self.get_object()
        user_org_id = self.request.user.profile.organization_id
        return user_org_id == organization.pk

    def get_queryset(self):
        return super().get_queryset().select_related("main_manager")

    def get_object(self, queryset=None):
        if not hasattr(self, "object") or self.object is None:
            self.object = super().get_object(queryset)

        return self.object


class OrganizationEditView(
    core.mixins.ForbiddenMixin,
    django.views.generic.UpdateView,
):
    model = company.models.Organization
    form_class = company.forms.OrganizationForm
    template_name = "company/organization_edit.html"
    context_object_name = "organization"

    def test_func(self):
        organization = self.get_object()
        user = self.request.user

        return (
            user.profile.organization == organization
            and user.profile.is_director
        )

    def get_success_url(self):
        return self.request.path


class GroupListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    model = company.models.WorkerGroup
    template_name = "company/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return (
            company.models.WorkerGroup.objects.filter(
                organization_id=self.request.user.profile.organization_id,
            )
            .select_related(
                "manager",
            )
            .annotate(
                workers_count=django.db.models.Count("workers"),
                org_name=django.db.models.F("organization__name"),
            )
        )


class GroupDetailView(
    core.mixins.ForbiddenMixin,
    django.views.generic.DetailView,
):
    model = company.models.WorkerGroup
    template_name = "company/group_detail.html"
    context_object_name = "group"

    def test_func(self):
        organization = self.get_object()
        user_org_id = self.request.user.profile.organization_id
        return user_org_id == organization.pk

    def get_queryset(self):
        return (
            company.models.WorkerGroup.objects.filter(
                organization_id=self.request.user.profile.organization_id,
            )
            .select_related(
                "manager",
                "organization",
            )
            .prefetch_related(
                "workers",
            )
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "object") or self.object is None:
            self.object = super().get_object(queryset)

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = self.get_object()
        user = self.request.user

        can_edit = user.profile.is_director or group.manager == user

        context["can_edit_group"] = can_edit
        return context


class GroupEditView(
    core.mixins.ForbiddenMixin,
    django.views.generic.UpdateView,
):
    model = company.models.WorkerGroup
    form_class = company.forms.WorkerGroupEditForm
    template_name = "company/group_edit.html"
    context_object_name = "group"

    def test_func(self):
        group = self.get_object()
        user = self.request.user

        if user.profile.organization.pk != group.organization.pk:
            return False

        is_group_manager = (
            user.profile.is_manager and group.manager.pk == user.pk
        )

        return user.profile.is_director or is_group_manager

    def get_success_url(self):
        return django.urls.reverse(
            "company:group_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class GroupCreateView(
    core.mixins.ForbiddenMixin,
    django.views.generic.CreateView,
):
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
