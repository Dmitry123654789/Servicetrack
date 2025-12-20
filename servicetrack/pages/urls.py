__all__ = ()

import django.urls

import pages.views

app_name = "pages"

urlpatterns = [
    django.urls.path(
        "",
        pages.views.HomePageView.as_view(),
        name="home",
    ),
    django.urls.path(
        "about/",
        pages.views.AboutPageView.as_view(),
        name="about",
    ),
]
