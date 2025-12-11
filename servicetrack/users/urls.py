__all__ = ()

import django.urls

from users import views

app_name = "users"

urlpatterns = [
    django.urls.path("login/", views.LoginView.as_view(), name="login"),
    django.urls.path("logout/", views.LogoutView.as_view(), name="logout"),
    django.urls.path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    django.urls.path(
        "password-change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    django.urls.path(
        "password-change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    django.urls.path(
        "password-reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    django.urls.path(
        "password-reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    django.urls.path("profile/", views.ProfileView.as_view(), name="profile"),
    django.urls.path(
        "profile/edit/",
        views.ProfileUpdateView.as_view(),
        name="profile_edit",
    ),
    django.urls.path(
        "create/",
        views.UserCreateView.as_view(),
        name="user_create",
    ),
    django.urls.path(
        "user-list/",
        views.UserListView.as_view(),
        name="user_list",
    ),
]
