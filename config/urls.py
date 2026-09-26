"""Root URL configuration for the Dairy Management System."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def health_check(request):
    """Lightweight endpoint for uptime monitors (Render health check)."""
    return HttpResponse("ok")


urlpatterns = [
    path("ok/", health_check, name="health"),
    path("admin/", admin.site.urls),
    path("", include("reports.urls")),
    path("accounts/", include("accounts.urls")),
    path("herd/", include("herd.urls")),
    path("milk/", include("milk.urls")),
    path("breeding/", include("breeding.urls")),
    path("health/", include("health.urls")),
    path("feed/", include("feed.urls")),
    path("inventory/", include("inventory.urls")),
    path("sales/", include("sales.urls")),
    path("purchases/", include("purchases.urls")),
    path("finance/", include("finance.urls")),
    path("employees/", include("employees.urls")),
    path("deliveries/", include("deliveries.urls")),
    path("invoicing/", include("invoicing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)