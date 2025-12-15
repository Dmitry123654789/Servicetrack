__all__ = ()

import django.apps
from django.utils.translation import gettext_lazy as _


class CompanyConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "company"
    verbose_name = _("Компания")
