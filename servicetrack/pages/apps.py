__all__ = ()

import django.apps
from django.utils.translation import gettext_lazy as _


class PagesConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    verbose_name = _("страницы")
