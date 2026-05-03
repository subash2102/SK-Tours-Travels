from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def staff_required(view_func):
    """
    Use for custom dashboard views. We intentionally rely on Django's `is_staff`
    to keep role-management simple and compatible with Django admin.
    """

    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Admin access required.")
        return view_func(request, *args, **kwargs)

    return _wrapped

