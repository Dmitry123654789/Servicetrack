__all__ = ()

import django.views.generic

import tickets.forms
import tickets.models
import users.models


class TicketListView(django.views.generic.ListView):
    model = tickets.models.Ticket
    template_name = "tickets/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 20

    def get_queryset(self):
        group_id = self.kwargs["pk"]

        qs = tickets.models.Ticket.objects.get_list().filter(group_id=group_id)
        return (
            qs.with_priority_weight()
            .with_status_weight()
            .sort(status="asc", priority="asc", created="asc")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = users.models.WorkerGroup.objects.get(
            pk=self.kwargs["pk"],
        )
        return context


class TicketDetailView(django.views.generic.DetailView):
    model = tickets.models.Ticket
    template_name = "tickets/ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        return self.model.objects.select_related(
            self.model.creator.field.name,
            self.model.assignee.field.name,
            self.model.group.field.name,
        ).prefetch_related(
            django.db.models.Prefetch(
                self.model.status_logs.field._related_name,
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logs"] = self.object.status_logs.all()
        context["logs"].order_by(  # noqa: ECE001
            f"-{tickets.models.StatusLog.timestamp.field.name}",
        )
        return context


class MyTicketListView(django.views.generic.TemplateView):
    model = tickets.models.Ticket
    template_name = "tickets/my_ticket_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        tickets_qs = self.model.objects.filter(assignee=user).select_related(
            self.model.group.field.name,
        )
        tickets_qs_sort = (
            tickets_qs.with_priority_weight()
            .with_status_weight()
            .sort(status="asc", priority="asc", created="asc")
        )

        groups = []

        for group in users.models.WorkerGroup.objects.filter(
            tickets__assignee=user,
        ).distinct():
            groups.append(
                {
                    "group": group,
                    "tickets": tickets_qs_sort.filter(group=group),
                },
            )

        context["groups"] = groups
        return context


class TicketCreateView(django.views.generic.CreateView):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketCreateForm
    template_name = "tickets/ticket_create.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TicketWorkerUpdateView(django.views.generic.UpdateView):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketWorkerForm
    template_name = "tickets/ticket_worker_update.html"

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


class TicketManagerUpdateView(django.views.generic.UpdateView):
    model = tickets.models.Ticket
    form_class = tickets.forms.TicketManagerForm
    template_name = "tickets/ticket_manager_update.html"

    def get_queryset(self):
        return self.model.objects.filter(group__manager=self.request.user)

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
