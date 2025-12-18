__all__ = ()

import collections

import django.contrib
import django.contrib.auth.mixins
import django.contrib.auth.views
import django.db.models
import django.urls
from django.utils.translation import gettext_lazy as _
import django.views.generic

import core.mixins
import users.forms
import users.models


class RegisterView(
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.CreateView,
):
    form_class = users.forms.CustomUserCreationForm
    template_name = "users/register.html"
    success_url = django.urls.reverse_lazy("users:login")

    def test_func(self):
        return not self.request.user.is_authenticated


class LoginView(django.contrib.auth.views.LoginView):
    form_class = users.forms.CustomAuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = django.urls.reverse_lazy("users:profile")


class LogoutView(django.contrib.auth.views.LogoutView):
    template_name = "users/logout.html"
    next_page = django.urls.reverse_lazy("users:login")


class PasswordChangeView(django.contrib.auth.views.PasswordChangeView):
    form_class = users.forms.CustomPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = django.urls.reverse_lazy("users:password_change_done")


class PasswordChangeDoneView(django.contrib.auth.views.PasswordChangeDoneView):
    template_name = "users/password_change_done.html"


class PasswordResetView(django.contrib.auth.views.PasswordResetView):
    form_class = users.forms.CustomPasswordResetForm
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = django.urls.reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(django.contrib.auth.views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class PasswordResetConfirmView(
    django.contrib.auth.views.PasswordResetConfirmView,
):
    form_class = users.forms.CustomSetPasswordForm
    template_name = "users/password_reset_confirm.html"
    success_url = django.urls.reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(
    django.contrib.auth.views.PasswordResetCompleteView,
):
    template_name = "users/password_reset_complete.html"


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.TemplateView,
):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context


class UserCreateView(
    core.mixins.ForbiddenMixin,
    django.views.generic.CreateView,
):
    form_class = users.forms.UserCreateForm
    template_name = "users/user_create.html"
    success_url = django.urls.reverse_lazy("users:user_list")

    def test_func(self):
        user = self.request.user
        return user.profile.role in [
            users.models.Profile.Role.MAIN_MANAGER,
            users.models.Profile.Role.GROUP_MANAGER,
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creator"] = self.request.user
        return kwargs

    def form_valid(self, form):
        django.contrib.messages.success(
            self.request,
            _("Пользователь_успешно_создан"),
        )
        return super().form_valid(form)


class UserListView(
    core.mixins.ForbiddenMixin,
    django.views.generic.ListView,
):
    model = users.models.CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        user = self.request.user
        return user.profile.role in [
            users.models.Profile.Role.MAIN_MANAGER,
            users.models.Profile.Role.GROUP_MANAGER,
        ]

    def get_queryset(self):
        user = self.request.user

        queryset = (
            super()
            .get_queryset()
            .select_related("profile")
            .prefetch_related("work_groups")
            .filter(
                profile__organization_id=user.profile.organization_id,
            )
        )

        queryset = queryset.exclude(
            profile__role=users.models.Profile.Role.MAIN_MANAGER,
        )

        if user.profile.is_manager:
            queryset = queryset.filter(
                django.db.models.Q(work_groups__manager_id=user.id)
                | django.db.models.Q(work_groups__isnull=True)
            ).distinct()

        return queryset.exclude(id=user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        grouped_dict = collections.defaultdict(list)
        for user in self.object_list:
            user_groups = user.work_groups.all()

            if user_groups:
                for group in user_groups:
                    if (
                        current_user.profile.is_director
                        or group.manager_id == current_user.id
                    ):
                        grouped_dict[group].append(user)
            else:
                grouped_dict["_no_group"].append(user)

        context["groups"] = [
            {
                "group": group,
                "users": user_list,
            }
            for group, user_list in grouped_dict.items()
        ]

        return context


class ProfileUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    form_class = users.forms.UserProfileUpdateForm
    template_name = "users/profile_edit.html"
    success_url = django.urls.reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        django.contrib.messages.success(
            self.request,
            _("Профиль_успешно_обновлен"),
        )
        return super().form_valid(form)
