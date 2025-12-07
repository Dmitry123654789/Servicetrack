__all__ = ()

from django.contrib import messages
import django.contrib.auth.mixins
from django.contrib.auth.mixins import UserPassesTestMixin
import django.contrib.auth.views
import django.urls
from django.utils.translation import gettext_lazy as _
import django.views.generic

from users import forms, models


class RegisterView(django.views.generic.CreateView):
    form_class = forms.CustomUserCreationForm
    template_name = "users/register.html"
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        if form.cleaned_data.get("phone"):
            self.object.profile.phone = form.cleaned_data["phone"]
            self.object.profile.save()

        return super().form_valid(form)


class LoginView(django.contrib.auth.views.LoginView):
    form_class = forms.CustomAuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return django.urls.reverse_lazy("users:profile")


class LogoutView(django.contrib.auth.views.LogoutView):
    template_name = "users/logout.html"
    next_page = django.urls.reverse_lazy("users:login")


class PasswordChangeView(django.contrib.auth.views.PasswordChangeView):
    form_class = forms.CustomPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = django.urls.reverse_lazy("users:password_change_done")


class PasswordChangeDoneView(django.contrib.auth.views.PasswordChangeDoneView):
    template_name = "users/password_change_done.html"


class PasswordResetView(django.contrib.auth.views.PasswordResetView):
    form_class = forms.CustomPasswordResetForm
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = django.urls.reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(django.contrib.auth.views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class PasswordResetConfirmView(
    django.contrib.auth.views.PasswordResetConfirmView,
):
    form_class = forms.CustomSetPasswordForm
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
    form_class = forms.UserCreateForm
    template_name = "users/user_create.html"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        profile = self.request.user.profile
        return profile.role in [
            models.Profile.Role.MAIN_MANAGER,
            models.Profile.Role.GROUP_MANAGER,
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
    model = models.CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        profile = self.request.user.profile
        return profile.role in [
            models.Profile.Role.MAIN_MANAGER,
            models.Profile.Role.GROUP_MANAGER,
        ]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("profile")

        if self.request.user.profile.role == models.Profile.Role.GROUP_MANAGER:
            managed_groups = models.WorkerGroup.objects.filter(
                manager=self.request.user,
            )
            worker_ids = set()
            for group in managed_groups:
                worker_ids.update(group.workers.values_list("id", flat=True))

            queryset = queryset.filter(
                id__in=worker_ids,
                profile__role=models.Profile.Role.WORKER,
            )

        return queryset.exclude(id=self.request.user.id)


class ProfileUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    form_class = forms.UserProfileUpdateForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Профиль успешно обновлен"))
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse_lazy("users:profile")
