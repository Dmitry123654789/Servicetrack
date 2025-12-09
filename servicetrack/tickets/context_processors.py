__all__ = ()


def user_groups(request):
    if not request.user.is_authenticated:
        return {}

    profile = request.user.profile

    if not profile.organization:
        return {"menu_groups": []}

    groups = profile.organization.groups.all()

    return {
        "menu_groups": groups,
    }
