__all__ = ()

import django.conf
import django.contrib
import django.contrib.admin
import django.urls

import pages.urls
import tickets.urls
import users.urls


urlpatterns = [
    django.urls.path("", django.urls.include(pages.urls)),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("auth/", django.urls.include(users.urls)),
    django.urls.path("tickets/", django.urls.include(tickets.urls)),
]

if django.conf.settings.DEBUG:
    import debug_toolbar.toolbar

    urlpatterns += debug_toolbar.toolbar.debug_toolbar_urls()
