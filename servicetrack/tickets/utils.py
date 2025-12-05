__all__ = ()

import django.utils


def item_directory_path(instance, filename, field_name):
    current_time = django.utils.timezone.now()
    return "{}/{}/{}/{}/{}/{}".format(
        instance._meta.app_label,
        field_name,
        current_time.strftime("%Y"),
        current_time.strftime("%m"),
        current_time.strftime("%d"),
        django.utils.text.get_valid_filename(filename),
    )


def get_photo_before_path(instance, filename):
    return item_directory_path(instance, filename, field_name="photo_before")


def get_photo_after_path(instance, filename):
    return item_directory_path(instance, filename, field_name="photo_after")
