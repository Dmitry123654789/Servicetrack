__all__ = ()

import django.contrib.admin
import django.contrib.auth.admin

import users.models


@django.contrib.admin.register(users.models.WorkerGroup)
class WorkerGroupAdmin(django.contrib.admin.ModelAdmin):
    model = users.models.WorkerGroup
    fields = (
        model.name.field.name,
        model.description.field.name,
        model.workers.field.name,
        model.manager.field.name,
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    readonly_fields = (
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    filter_horizontal = (model.workers.field.name,)


class ProfileInline(django.contrib.admin.StackedInline):
    model = users.models.Profile
    can_delete = False

    fields = (
        model.role.field.name,
        model.phone.field.name,
    )


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    model = users.models.CustomUser
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    model.username.field.name,
                    model.email.field.name,
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = (ProfileInline,)


django.contrib.admin.site.register(
    users.models.CustomUser,
    UserAdmin,
)
