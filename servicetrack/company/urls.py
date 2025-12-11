__all__ = ()

import django.urls

from company import views

app_name = "company"

urlpatterns = [
    django.urls.path(
        "organization-detail/<int:pk>/",
        views.OrganizationView.as_view(),
        name="organization_detail",
    ),
    django.urls.path(
        "organization-edit/<int:pk>/",
        views.OrganizationEditView.as_view(),
        name="organization_edit",
    ),
    django.urls.path(
        "group-detail/<int:pk>/",
        views.GroupDetailView.as_view(),
        name="group_detail",
    ),
    django.urls.path(
        "group-edit/<int:pk>/",
        views.GroupEditView.as_view(),
        name="group_edit",
    ),
    django.urls.path(
        "group-list/",
        views.GroupListView.as_view(),
        name="group_list",
    ),
    django.urls.path(
        "group-create/",
        views.GroupCreateView.as_view(),
        name="group_create",
    ),
]
