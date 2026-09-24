"""Context processors available to every template."""

from accounts.models import FarmProfile


def site_context(request):
    """Expose the farm profile and app metadata in the template context."""
    farm = None
    if getattr(request, "user", None) and request.user.is_authenticated:
        farm = FarmProfile.objects.filter(user=request.user).first()
    return {"farm": farm, "app_name": "Dairy Manager"}