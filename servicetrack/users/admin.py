__all__ = ()

import django.contrib.admin
import django.contrib.auth.admin

import users.models


class ProfileInline(django.contrib.admin.StackedInline):
    model = users.models.Profile
    can_delete = False

    fields = (
        model.role.field.name,
        model.phone.field.name,
    )


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


django.contrib.admin.site.register(
    users.models.CustomUser,
    UserAdmin,
)
