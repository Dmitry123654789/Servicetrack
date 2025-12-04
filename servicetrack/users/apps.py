__all__ = ()

import django.apps
import django.db.models.signals
from django.utils.translation import gettext_lazy as _


class UsersConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = _("пользователи")

    def ready(self):
        from django.contrib.auth import get_user_model
        import users.signals

        user = get_user_model()
        django.db.models.signals.post_save.connect(
            users.signals.create_user_profile,
            sender=user,
        )
