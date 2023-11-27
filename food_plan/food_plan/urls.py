from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('api/v1/admin', admin.site.urls),
    path("api/v1/", include("mainapp.urls")),
    path("api/v1/user/", include("userapp.urls")),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
]

urlpatterns += doc_urls

# это нужно для отображения картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
