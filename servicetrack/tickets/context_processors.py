__all__ = ()

import django.db.models

import company.models


def user_groups(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    organization_id = user.profile.organization_id

    if not organization_id:
        return {"menu_groups": []}

    user_groups = company.models.WorkerGroup.objects.filter(
        organization_id=organization_id,
    )
    if not user.profile.is_director:
        user_groups = user_groups.filter(
            django.db.models.Q(workers=user)
            | django.db.models.Q(manager=user),
        )

    return {
        "menu_groups": user_groups.distinct(),
    }
