__all__ = ()

import django.contrib.admin

import company.models


@django.contrib.admin.register(company.models.WorkerGroup)
class WorkerGroupAdmin(django.contrib.admin.ModelAdmin):
    model = company.models.WorkerGroup
    fields = (
        model.name.field.name,
        model.description.field.name,
        model.workers.field.name,
        model.manager.field.name,
        model.organization.field.name,
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    readonly_fields = (
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    filter_horizontal = (model.workers.field.name,)

    list_display = (
        model.name.field.name,
        model.manager.field.name,
        model.organization.field.name,
    )


@django.contrib.admin.register(company.models.Organization)
class OrganizationAdmin(django.contrib.admin.ModelAdmin):
    model = company.models.Organization
    fields = (
        model.name.field.name,
        model.description.field.name,
        model.main_manager.field.name,
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    readonly_fields = (
        model.created_at.field.name,
        model.updated_at.field.name,
    )

    list_display = (
        model.name.field.name,
        model.main_manager.field.name,
    )
