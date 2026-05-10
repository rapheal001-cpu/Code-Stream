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
from django.views import View
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
    course_view,
)


# ====================
# AUTHENTICATION VIEWS
# ====================
class CustomSignupView(SignupView):
    """User registration view"""

    template_name = "accounts/account/signup.html"


signup_view = CustomSignupView.as_view()


class CustomLoginView(LoginView):
    """User login view"""

    template_name = "accounts/account/login.html"


login_view = CustomLoginView.as_view()


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """User logout view"""

    template_name = "accounts/account/logout.html"
    next_page = reverse_lazy(index_view)


logout_view = CustomLogoutView.as_view()


# ===========
# EMAIL VIEWS
# ===========
class CustomEmailVerificationSentView(EmailVerificationSentView):
    """Email verification sent confirmation"""

    template_name = "accounts/account/email_verification_sent.html"


email_verification_sent_view = CustomEmailVerificationSentView.as_view()


class CustomConfirmEmailView(ConfirmEmailView):
    """Email confirmation handler"""

    template_name = "accounts/account/confirm_email.html"


confirm_email_view = CustomConfirmEmailView.as_view()


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


email_view = CustomEmailView.as_view()


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


password_change_view = CustomPasswordChangeView.as_view()


class CustomPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """Password change success view"""

    template_name = "accounts/account/password_change_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


password_change_done_view = CustomPasswordChangeDoneView.as_view()


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    """Initial password set (social auth users)"""

    template_name = "accounts/socialaccount/password_set.html"
    success_url = reverse_lazy("password_set_done")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


password_set_view = CustomPasswordSetView.as_view()


class CustomPasswordSetDoneView(LoginRequiredMixin, TemplateView):
    """Password set success view"""

    template_name = "accounts/socialaccount/password_set_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


password_set_done_view = CustomPasswordSetDoneView.as_view()


class CustomPasswordResetView(PasswordResetView):
    """Password reset request view"""

    template_name = "accounts/account/password_reset.html"


password_reset_view = CustomPasswordResetView.as_view()


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset email sent view"""

    template_name = "accounts/account/password_reset_done.html"


password_reset_done_view = CustomPasswordResetDoneView.as_view()


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    """Password reset from email link"""

    template_name = "accounts/account/password_reset_from_key.html"
    success_url = reverse_lazy("account_reset_password_from_key_done")


password_reset_from_key_view = CustomPasswordResetFromKeyView.as_view()


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    """Password reset completion view"""

    template_name = "accounts/account/password_reset_from_key_done.html"


password_reset_from_key_done_view = CustomPasswordResetFromKeyDoneView.as_view()

# =================
# SOCIAL AUTH VIEWS
# =================
class CustomLoginCancelledView(LoginCancelledView):
    """Social login cancelled handler"""

    template_name = "accounts/socialaccount/login_cancelled.html"


login_cancelled_view = CustomLoginCancelledView.as_view()


class CustomLoginErrorView(LoginErrorView):
    """Social login error handler"""

    template_name = "accounts/socialaccount/authentication_error.html"


login_error_view = CustomLoginErrorView.as_view()


class CustomSocialConnectionsView(LoginRequiredMixin, ConnectionsView):
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


social_connections_view = CustomSocialConnectionsView.as_view()

# ==================
# USER PROFILE VIEWS
# ==================
class ProfileView(LoginRequiredMixin, DetailView):
    """Public profile display with view tracking"""

    model = User
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "accounts/user/main/profile.html"

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


profile_view = ProfileView.as_view()


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Profile updating view"""

    model = User
    form_class = UpdateProfileForm
    template_name = "accounts/user/main/update_profile.html"
    success_url = reverse_lazy("settings")

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


update_profile_view = UpdateProfileView.as_view()


class DescriptionView(LoginRequiredMixin, UpdateView):
    """User description/bio editing"""

    model = User
    form_class = ProfileDescriptionForm
    template_name = "accounts/user/main/description.html"
    success_url = reverse_lazy("settings")

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


description_view = DescriptionView.as_view()


class SettingsView(LoginRequiredMixin, DetailView):
    """User settings page"""

    model = User
    context_object_name = "user"
    template_name = "accounts/user/main/settings.html"

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


settings_view = SettingsView.as_view()


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


profile_views_list = ProfileViewsList.as_view()


# ==================
# NOTIFICATION VIEWS
# ==================
class NotificationView(LoginRequiredMixin, ListView):
    """User notifications list"""

    model = Notification
    fields = "__all__"
    context_object_name = "notifications"
    template_name = "accounts/user/main/notification.html"

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


notification_view = NotificationView.as_view()


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


notification_detail_view = NotificationDetailView.as_view()


# ===================
# SOCIAL/FRIEND VIEWS
# ===================
class FindFriendView(LoginRequiredMixin, TemplateView):
    """Search and follow/unfollow users"""

    template_name = "accounts/user/main/find_friend.html"

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


find_friend_view = FindFriendView.as_view()


# =======================
# INSTRUCTOR WALLET VIEWS
# =======================
class InstructorWalletView(LoginRequiredMixin, DetailView):
    model = Wallet
    fields = "__all__"
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "wallet"
    template_name = "accounts/user/main/wallet.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        self.object = self.get_object()
        wallet = self.object
        if not user.role or wallet.user.pk != user.pk:
            return redirect(index_view)
        return super().get(request, *args, **kwargs)


instructor_wallet_view = InstructorWalletView.as_view()


# ========================
# INSTRUCTOR Courses VIEWS
# ========================
class InstructorCoursesView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user/main/instructor_courses.html"

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


instructor_course_view = InstructorCoursesView.as_view()


# ========================
# Follow and Unfollow VIEWS
# ========================
class FollowView(LoginRequiredMixin, View):
    def post(self, request, pk=None, *args, **kwargs):
        user_to_follow = get_object_or_404(User, pk=pk)
        current_user = request.user

        # Prevent self-follow
        if current_user == user_to_follow:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Unfollow
        if current_user in user_to_follow.followers.all():
            user_to_follow.followers.remove(current_user)

        # Follow
        else:
            user_to_follow.followers.add(current_user)

            # Prevent duplicate notifications
            Notification.objects.create(
                user=user_to_follow,
                title="New Follower",
                sender=current_user,
                message=f"@{current_user.username} started following you.",
            )

        return redirect(request.META.get("HTTP_REFERER", "/"))


follow_view = FollowView.as_view()


# ========================
# Followers and Following VIEWS
# ========================
class FollowersAndFollowingView(LoginRequiredMixin, DetailView):
    model = User
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "user"
    template_name = "accounts/user/main/followers_and_following.html"

followers_and_following_view = FollowersAndFollowingView.as_view()


class FollowersView(LoginRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        followers = user.followers.all()
        context = {"followers": followers}
        if request.htmx:
            return render(request, 'accounts/user/partials/followers.html', context)
        return render(request, 'accounts/user/main/followers_and_following.html', context)


followers_view = FollowersView.as_view()


class FollowingView(LoginRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        following = user.following.all()
        context = {"following": following}
        if request.htmx:
            return render(request, 'accounts/user/partials/following.html', context)
        return render(request, 'accounts/user/main/followers_and_following.html', context)


following_view = FollowingView.as_view()