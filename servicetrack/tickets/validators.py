__all__ = ()

import django.core.exceptions
import django.template.defaultfilters
import django.utils.deconstruct
from django.utils.translation import gettext_lazy as _


@django.utils.deconstruct.deconstructible
class FileValidator(object):
    max_size_message = _(
        "Текущий_файл_%(size)s,_слишком_большой._"
        "Максимальный_размер_файла_%(allowed_size)s.",
    )

    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop("max_size", None)

    def __call__(self, value):
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                "size": django.template.defaultfilters.filesizeformat(
                    filesize,
                ),
                "allowed_size": django.template.defaultfilters.filesizeformat(
                    self.max_size,
                ),
            }

            raise django.core.exceptions.ValidationError(message)
