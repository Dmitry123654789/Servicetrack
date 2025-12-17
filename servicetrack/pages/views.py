__all__ = ()

import django.views.generic


class HomePageView(django.views.generic.TemplateView):
    template_name = "pages/home.html"


class AboutPageView(django.views.generic.TemplateView):
    template_name = "pages/about.html"


class ContactPageView(django.views.generic.TemplateView):
    template_name = "pages/contact.html"
