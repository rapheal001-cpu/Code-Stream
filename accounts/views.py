from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView,
    TemplateView,
)
from django.db.models import Q
from allauth.account.views import (
    LoginView,
    LogoutView,
    SignupView,
    PasswordChangeView,
    PasswordSetView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    EmailView,
    ConfirmEmailView,
    EmailVerificationSentView,
)
from allauth.socialaccount.views import (
    ConnectionsView,
    LoginCancelledView,
    LoginErrorView,
)
from allauth.account.models import EmailAddress
from .models import (
    User,
    Notification,
    Wallet,
)
from .forms import (
    UpdateProfileForm,
    ProfileDescriptionForm,
)
from course.models import Course
from CodeStream.utils import (
    index_view,
    notification_view,
    find_friend_view,
    course_view,
)


# ====================
# AUTHENTICATION VIEWS
# ====================
class CustomSignupView(SignupView):
    """User registration view"""

    template_name = "accounts/account/signup.html"


class CustomLoginView(LoginView):
    """User login view"""

    template_name = "accounts/account/login.html"


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """User logout view"""

    template_name = "accounts/account/logout.html"
    next_page = reverse_lazy("account_login")


# ===========
# EMAIL VIEWS
# ===========
class CustomEmailVerificationSentView(EmailVerificationSentView):
    """Email verification sent confirmation"""

    template_name = "accounts/account/email_verification_sent.html"


class CustomConfirmEmailView(ConfirmEmailView):
    """Email confirmation handler"""

    template_name = "accounts/account/confirm_email.html"


class CustomEmailView(LoginRequiredMixin, EmailView):
    """Email management view"""

    template_name = "accounts/account/change_email.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["email_addresses"] = EmailAddress.objects.filter(user=user)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


# ==============
# PASSWORD VIEWS
# ==============
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Password change view"""

    template_name = "accounts/account/password_change.html"
    success_url = reverse_lazy("password_change_done")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class CustomPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """Password change success view"""

    template_name = "accounts/account/password_change_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    """Initial password set (social auth users)"""

    template_name = "accounts/socialaccount/password_set.html"
    success_url = reverse_lazy("password_set_done")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class CustomPasswordSetDoneView(LoginRequiredMixin, TemplateView):
    """Password set success view"""

    template_name = "accounts/socialaccount/password_set_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """Password reset request view"""

    template_name = "accounts/account/password_reset.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset email sent view"""

    template_name = "accounts/account/password_reset_done.html"


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    """Password reset from email link"""

    template_name = "accounts/account/password_reset_from_key.html"
    success_url = reverse_lazy("account_reset_password_from_key_done")


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    """Password reset completion view"""

    template_name = "accounts/account/password_reset_from_key_done.html"


# =================
# SOCIAL AUTH VIEWS
# =================
class CustomLoginCancelledView(LoginCancelledView):
    """Social login cancelled handler"""

    template_name = "accounts/socialaccount/login_cancelled.html"


class CustomLoginErrorView(LoginErrorView):
    """Social login error handler"""

    template_name = "accounts/socialaccount/authentication_error.html"


class CustomConnectionsView(LoginRequiredMixin, ConnectionsView):
    """Social account management"""

    template_name = "accounts/socialaccount/social_account_connections.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["connected_providers"] = [
            account.provider for account in context["form"].accounts
        ]
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect("core:index-view")
        return super().get(request, *args, **kwargs)


# ==================
# USER PROFILE VIEWS
# ==================
class ProfileView(LoginRequiredMixin, DetailView):
    """Public profile display with view tracking"""

    model = User
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "accounts/user/html/profile.html"

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        viewer = request.user

        if not request.user.role:
            return redirect(index_view)

        if viewer != profile:
            if not profile.profile_views.filter(pk=viewer.pk).exists():
                profile.profile_views.add(viewer)
                Notification.objects.create(
                    user=profile,
                    title="Profile view",
                    message=f"@{viewer.username} just viewed your profile.",
                )

        return super().get(request, *args, **kwargs)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Profile updating view"""

    model = User
    form_class = UpdateProfileForm
    template_name = "accounts/user/html/update_profile.html"
    success_url = reverse_lazy("settings")

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class DescriptionView(LoginRequiredMixin, UpdateView):
    """User description/bio editing"""

    model = User
    form_class = ProfileDescriptionForm
    template_name = "accounts/user/html/description.html"
    success_url = reverse_lazy("settings")

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class SettingsView(LoginRequiredMixin, DetailView):
    """User settings page"""

    model = User
    context_object_name = "user"
    template_name = "accounts/user/html/settings.html"

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


class ProfileViewsList(LoginRequiredMixin, DetailView):
    """List of users who viewed profile"""

    model = User
    context_object_name = "profile_user"
    template_name = "accounts/user/partials/profile_views.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profile = self.get_object()
        context["viewer"] = profile.profile_views.exclude(pk=profile.pk)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


# ==================
# NOTIFICATION VIEWS
# ==================
class NotificationView(LoginRequiredMixin, ListView):
    """User notifications list"""

    model = Notification
    fields = "__all__"
    context_object_name = "notifications"
    template_name = "accounts/user/html/notification.html"

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        delete_notification = request.POST.get("delete_id")
        user = request.user
        notification = get_object_or_404(
            Notification, pk=delete_notification, user=user
        )
        notification.delete()
        return redirect(notification_view)


class NotificationDetailView(LoginRequiredMixin, DetailView):
    """Single notification detail"""

    model = Notification
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "notification"
    template_name = "accounts/user/partials/notification_detail.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect("core:index-view")
        notification = get_object_or_404(
            Notification, pk=self.kwargs.get(self.pk_url_kwarg), user=self.request.user
        )
        if notification and not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return super().get(request, *args, **kwargs)


# ===================
# SOCIAL/FRIEND VIEWS
# ===================
class FindFriendView(LoginRequiredMixin, TemplateView):
    """Search and follow/unfollow users"""

    template_name = "accounts/user/html/find_friend.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)

        search = request.GET.get("search")
        user = self.request.user

        if search:
            friends = User.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(username__icontains=search)
            ).exclude(id=user.id)
        else:
            friends = User.objects.exclude(id=user.id)

        context = {"search": search, "friends": friends}

        if request.htmx:
            return render(
                request, "accounts/user/partials/find_friend_list.html", context
            )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        friend_username = request.POST.get("friend_username").strip()
        user = request.user

        friend = get_object_or_404(User, username=friend_username)

        if user in friend.followers.all():
            friend.followers.remove(user)
        else:
            friend.followers.add(user)

        return redirect(find_friend_view)


# =======================
# INSTRUCTOR WALLET VIEWS
# =======================
class InstructorWalletView(LoginRequiredMixin, DetailView):
    model = Wallet
    fields = "__all__"
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "wallet"
    template_name = "accounts/user/html/wallet.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        self.object = self.get_object()
        wallet = self.object
        if not user.role or wallet.user.pk != user.pk:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


# ========================
# INSTRUCTOR Courses VIEWS
# ========================
class InstructorCoursesView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/html/instructor_courses.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        search = request.GET.get("search")
        if user != user:
            return redirect(course_view)

        if search:
            courses = Course.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            ).order_by("-created_at")
        else:
            courses = Course.objects.filter(instructor=user).order_by("-created_at")

        context = {
            "courses": courses,
            "search": search,
        }

        if request.htmx:
            return render(request, "course/course/partials/courses_list.html", context)

        return render(request, self.template_name, context)
