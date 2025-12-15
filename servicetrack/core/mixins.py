__all__ = ()

import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import sorl.thumbnail


class ForbiddenMixin(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
):
    fallback_url = django.urls.reverse_lazy("pages:home")

    def handle_no_permission(self):
        return django.shortcuts.redirect(self.fallback_url)


class ImageCleanupMixin:
    IMAGE_FIELDS = []

    def _delete_old_image(self, field_name):
        if self.pk:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                old_file = getattr(old_instance, field_name)
            except self.__class__.DoesNotExist:
                return

            current_file = getattr(self, field_name)

            if old_file:
                if not current_file:
                    sorl.thumbnail.delete(old_file)
                elif old_file != current_file:
                    sorl.thumbnail.delete(old_file)

    def _delete_all_images(self, field_name):
        file_field = getattr(self, field_name)
        if file_field:
            sorl.thumbnail.delete(file_field)

    def save(self, *args, **kwargs):
        for field_name in self.IMAGE_FIELDS:
            self._delete_old_image(field_name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for field_name in self.IMAGE_FIELDS:
            self._delete_all_images(field_name)

        super().delete(*args, **kwargs)
