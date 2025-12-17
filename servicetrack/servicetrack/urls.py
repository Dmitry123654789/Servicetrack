__all__ = ()

import django.conf
import django.conf.urls.i18n
import django.conf.urls.static
import django.contrib
import django.contrib.admin
import django.urls

import company.urls
import pages.urls
import tickets.urls
import users.urls


urlpatterns = [
    django.urls.path("", django.urls.include(pages.urls)),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("auth/", django.urls.include(users.urls)),
    django.urls.path("company/", django.urls.include(company.urls)),
    django.urls.path("tickets/", django.urls.include(tickets.urls)),
    django.urls.path("i18n/", django.urls.include(django.conf.urls.i18n)),
]

if django.conf.settings.DEBUG:
    import debug_toolbar.toolbar

    urlpatterns += debug_toolbar.toolbar.debug_toolbar_urls()

    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.STATIC_URL,
        document_root=django.conf.settings.STATIC_ROOT,
    )

    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
