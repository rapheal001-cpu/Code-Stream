from django.shortcuts import (
    redirect,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)
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
from CodeStream.utils import (
    index_view_url,
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
    next_page = reverse_lazy(index_view_url)

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
            return redirect(index_view_url)
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
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

password_change_view = CustomPasswordChangeView.as_view()


class CustomPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """Password change success view"""
    template_name = "accounts/account/password_change_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

password_change_done_view = CustomPasswordChangeDoneView.as_view()


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    """Initial password set (social auth users)"""
    template_name = "accounts/socialaccount/password_set.html"
    success_url = reverse_lazy("password_set_done")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

password_set_view = CustomPasswordSetView.as_view()


class CustomPasswordSetDoneView(LoginRequiredMixin, TemplateView):
    """Password set success view"""
    template_name = "accounts/socialaccount/password_set_done.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
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
    """Social login canceled handler"""
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
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

social_connections_view = CustomSocialConnectionsView.as_view()