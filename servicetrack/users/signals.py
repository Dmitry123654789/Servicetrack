__all__ = ()

import users.models


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        users.models.Profile.objects.create(user=instance)
