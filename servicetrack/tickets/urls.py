__all__ = ()

import django.urls

import tickets.views

app_name = "tickets"

urlpatterns = [
    django.urls.path(
        "group/<int:pk>/",
        tickets.views.TicketListView.as_view(),
        name="tickets_list",
    ),
    django.urls.path(
        "my/",
        tickets.views.MyTicketListView.as_view(),
        name="my_tickets",
    ),
    django.urls.path(
        "detail/<int:pk>/",
        tickets.views.TicketDetailView.as_view(),
        name="ticket_detail",
    ),
    django.urls.path(
        "create/",
        tickets.views.TicketCreateView.as_view(),
        name="ticket_create",
    ),
    django.urls.path(
        "update/<int:pk>/",
        tickets.views.TicketWorkerUpdateView.as_view(),
        name="ticket_worker_update",
    ),
    django.urls.path(
        "edit/<int:pk>/",
        tickets.views.TicketManagerUpdateView.as_view(),
        name="ticket_manager_update",
    ),
]
