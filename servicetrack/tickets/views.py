__all__ = ()

import collections

import django.db.models
import django.db.transaction
import django.views.generic

import company.models
import core.mixins
import tickets.forms
import tickets.models
import users.models


class TicketListView(
    core.mixins.ForbiddenMixin,
    django.views.generic.ListView,
):
    model = tickets.models.Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 20

    def test_func(self):
        user = self.request.user
        group_pk = self.kwargs.get("pk")

        try:
            group = company.models.WorkerGroup.objects.get(
                pk=group_pk,
                organization_id=user.profile.organization_id,
            )
            self.group = group
        except company.models.WorkerGroup.DoesNotExist:
            return False

        if user.profile.organization_id != group.organization_id:
            return False

        if user.profile.is_director or group.manager_id == user.id:
            return True

        return group.workers.filter(pk=user.id).exists()

    def get_queryset(self):
        return (
            tickets.models.Ticket.objects.get_list()
            .filter(group_id=self.kwargs["pk"])
            .select_related("assignee")
            .with_priority_weight()
            .with_status_weight()
            .sort(status="asc", priority="asc", created="asc")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        return context


class TicketDetailView(
    core.mixins.ForbiddenMixin,
    django.views.generic.DetailView,
):
    model = tickets.models.Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def test_func(self):
        user = self.request.user
        profile = user.profile

        ticket = self.get_object()
        target_group = ticket.group

        if profile.organization_id != target_group.organization_id:
            return False

        if profile.is_director or target_group.manager_id == user.id:
            return True

        return target_group.workers.filter(pk=user.id).exists()

    def get_queryset(self):
        return self.model.objects.select_related(
            self.model.creator.field.name,
            self.model.assignee.field.name,
            self.model.group.field.name,
        ).select_related(
            "group__organization",
        ).prefetch_related(
            django.db.models.Prefetch(
                self.model.status_logs.field._related_name,
            ),
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "object") or self.object is None:
            self.object = super().get_object(queryset)

        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logs"] = self.object.status_logs.order_by(
            f"-{tickets.models.StatusLog.timestamp.field.name}",
        )
        return context


class MyTicketListView(
    core.mixins.ForbiddenMixin,
    django.views.generic.TemplateView,
):
    model = tickets.models.Ticket
    template_name = "tickets/my_ticket_list.html"

    def test_func(self):
        user = self.request.user
        return user.profile.role in [
            users.models.Profile.Role.WORKER,
            users.models.Profile.Role.GROUP_MANAGER,
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        tickets_qs = self.model.objects.filter(assignee=user).select_related(
            self.model.group.field.name,
            self.model.assignee.field.name,
        )
        tickets_qs_sort = (
            tickets_qs.with_priority_weight()
            .with_status_weight()
            .sort(status="asc", priority="asc", created="asc")
        )

        grouped_tickets = collections.defaultdict(list)
        for ticket in tickets_qs_sort:
            grouped_tickets[ticket.group].append(ticket)

        groups_list = []
        for group, ticket_list in grouped_tickets.items():
            groups_list.append(
                {
                    "group": group,
                    "tickets": ticket_list,
                },
            )

        context["groups"] = groups_list
        return context


class TicketCreateView(
    core.mixins.ForbiddenMixin,
    django.views.generic.CreateView,
):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketCreateForm
    template_name = "tickets/ticket_create.html"

    def test_func(self):
        user = self.request.user
        return user.profile.role in [
            users.models.Profile.Role.GROUP_MANAGER,
            users.models.Profile.Role.WORKER,
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TicketWorkerUpdateView(
    core.mixins.ForbiddenMixin,
    django.views.generic.UpdateView,
):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketWorkerForm
    template_name = "tickets/ticket_worker_update.html"

    def test_func(self):
        ticket = self.get_object()
        return ticket in self.model.objects.filter(assignee=self.request.user)

    def get_queryset(self):
        return self.model.objects.filter(assignee=self.request.user)

    def form_valid(self, form):
        ticket = self.get_object()
        old_status = ticket.status

        new_status = form.instance.status
        comment = form.cleaned_data.get("comment")

        if old_status != new_status:
            tickets.models.StatusLog.objects.create(
                ticket=ticket,
                user=self.request.user,
                from_status=old_status,
                to_status=new_status,
                comment=comment,
            )

        return super().form_valid(form)


class TicketManagerUpdateView(
    core.mixins.ForbiddenMixin,
    django.views.generic.UpdateView,
):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketManagerForm
    template_name = "tickets/ticket_manager_update.html"

    def test_func(self):
        user = self.request.user
        ticket = self.get_object()
        is_group_mgr = ticket.group.manager_id == user.id
        is_org_mgr = ticket.group.organization.main_manager_id == user.id
        return is_group_mgr or is_org_mgr

    def get_queryset(self):
        user_id = self.request.user.id

        return self.model.objects.filter(
            django.db.models.Q(group__manager_id=user_id)
            | django.db.models.Q(group__organization__main_manager_id=user_id),
        )

    def get_object(self, queryset=None):
        if not hasattr(self, "object") or self.object is None:
            self.object = super().get_object(queryset)

        return self.object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        with django.db.transaction.atomic():
            ticket = self.get_object()
            old_status = ticket.status

            new_status = form.instance.status
            comment = form.cleaned_data.get("comment")

            if old_status != new_status:
                tickets.models.StatusLog.objects.create(
                    ticket=ticket,
                    user=self.request.user,
                    from_status=old_status,
                    to_status=new_status,
                    comment=comment,
                )

            return super().form_valid(form)
