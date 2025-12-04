__all__ = ()

import django.conf
import django.contrib
import django.urls

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("auth/", django.urls.include("users.urls")),
    django.urls.path("", django.urls.include("pages.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar.toolbar

    urlpatterns += debug_toolbar.toolbar.debug_toolbar_urls()
