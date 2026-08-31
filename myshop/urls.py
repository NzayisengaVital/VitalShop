from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def ads_txt(request):
    content = "google.com, pub-9976796127860345, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),

    path('ads.txt', ads_txt, name='ads_txt'),

    path("", include("buy.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)