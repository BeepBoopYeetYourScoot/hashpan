from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blacklistedCards import settings
from hashpan_checker.urls import urlpatterns as hashpan_urls

urlpatterns = [path("admin/", admin.site.urls), path("", include(hashpan_urls))]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
