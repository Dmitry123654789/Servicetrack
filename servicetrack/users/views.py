__all__ = ()

from django.contrib import messages
import django.contrib.auth.mixins
from django.contrib.auth.mixins import UserPassesTestMixin
import django.contrib.auth.views
import django.urls
from django.utils.translation import gettext_lazy as _
import django.views.generic

import company.models
import users.forms
import users.models


class RegisterView(django.views.generic.CreateView):
    form_class = users.forms.CustomUserCreationForm
    template_name = "users/register.html"
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        organization = company.models.Organization.objects.create(
            name=form.cleaned_data["organization_name"],
            main_manager=user,
        )

        user.refresh_from_db()
        user.profile.phone = form.cleaned_data.get("phone", None)
        user.profile.organization = organization
        user.profile.role = users.models.Profile.Role.MAIN_MANAGER
        user.profile.save()

        return super().form_valid(form)


class LoginView(django.contrib.auth.views.LoginView):
    form_class = users.forms.CustomAuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return django.urls.reverse_lazy("users:profile")


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


class UserCreateView(UserPassesTestMixin, django.views.generic.CreateView):
    form_class = users.forms.UserCreateForm
    template_name = "users/user_create.html"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        profile = self.request.user.profile
        return profile.role in [
            users.models.Profile.Role.MAIN_MANAGER,
            users.models.Profile.Role.GROUP_MANAGER,
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creator"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно создан"))
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse_lazy("users:user_list")


class UserListView(UserPassesTestMixin, django.views.generic.ListView):
    model = users.models.CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        profile = self.request.user.profile
        return profile.role in [
            users.models.Profile.Role.MAIN_MANAGER,
            users.models.Profile.Role.GROUP_MANAGER,
        ]

    def get_queryset(self):
        user = self.request.user

        queryset = (
            super()
            .get_queryset()
            .select_related("profile")
            .filter(profile__organization=user.profile.organization)
        )

        if user.profile.is_manager:
            queryset = queryset.filter(
                work_groups__manager=user,
            ).distinct()

        return queryset.exclude(id=user.id)


class ProfileUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    form_class = users.forms.UserProfileUpdateForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Профиль_успешно_обновлен"))
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse_lazy("users:profile")
