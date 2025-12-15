__all__ = ()

import django.db.models

import company.models


def user_groups(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    if not user.profile.organization:
        return {"menu_groups": []}

    organization = user.profile.organization

    user_groups = company.models.WorkerGroup.objects.filter(
        organization=organization,
    )
    if not user.profile.is_director:
        user_groups = user_groups.filter(
            django.db.models.Q(workers=user)
            | django.db.models.Q(manager=user),
        )

    groups = user_groups.select_related("manager").distinct()

    return {
        "menu_groups": groups,
    }
