from CodeStream.utils import index_view_url
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


# ===================================================================================

# ======================
# Role Restriction Views
# ======================
class RoleRequiredMixin(AccessMixin):
    """Redirect to home if user has no role set."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role not in ['instructor', 'student']:
            return redirect(index_view_url)
        return super().dispatch(request, *args, **kwargs)

# ============================
# Instructor Restriction Views
# ============================
class InstructorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'instructor':
            return redirect(index_view_url)
        return super().dispatch(request, *args, **kwargs)

# =========================
# Student Restriction Views
# =========================
class StudentRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'student':
            return redirect(index_view_url)
        return super().dispatch(request, *args, **kwargs)

# ===================================================================================
