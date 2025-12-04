__all__ = ()

from django.utils.translation import gettext_lazy as _
import django.views.generic


class HomePageView(django.views.generic.TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Главная страница")
        return context


class AboutPageView(django.views.generic.TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("О проекте")
        return context


class ContactPageView(django.views.generic.TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Контакты")
        return context
