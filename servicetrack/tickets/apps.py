__all__ = ()

import django.apps
from django.utils.translation import gettext_lazy as _


class TicketsConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tickets"
    verbose_name = _("страницы")
