from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Limitless Admin"
admin.site.site_title = "Limitless"

urlpatterns = [
    path(r"staff/", admin.site.urls),
    path(r"", include("limitless.common.favicon_urls")),
    path(r"", include("limitless.common.urls")),
]
