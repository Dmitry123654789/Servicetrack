__all__ = ()

import django.contrib.auth.mixins
import django.contrib.auth.views
import django.urls
import django.views.generic

from users import forms


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
