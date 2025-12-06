__all__ = ()


def user_groups(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    groups = (user.work_groups.all() | user.managed_groups.all()).distinct()

    return {
        "menu_groups": groups,
    }
