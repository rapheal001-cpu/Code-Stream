from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView, ListView
from accounts.models import User, Notification, Wallet
from django.db.models import Q
from .models import Report
from .forms import UserRoleForm, UpdateProfileForm, ProfileDescriptionForm
from course.models import Course
from CodeStream.utils import about_view_url, index_view_url, notification_view_url, course_view_url, setting_view_url
from .tasks import create_instructor_wallet

# Create your views here.


# Landing Page View
class IndexView(TemplateView):
    template_name = "core/main/index.html"

    def get(self, request, *args, **kwargs):
        form = UserRoleForm()
        instructors = User.objects.filter(role="instructor").order_by("-last_login")
        search = request.GET.get("search")

        if search:
            courses = Course.objects.filter(Q(name__icontains=search)).order_by(
                "-created_at"
            )
        else:
            courses = Course.objects.order_by("-created_at")

        context = {"form": form, "instructors": instructors, "courses": courses}

        if request.htmx:
            return render(request, "core/partials/index_content.html", context)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            if user.role:
                Notification.objects.create(
                    user=user,
                    name="You're all set!",
                    message=f"Welcome to Code Stream, {user.full_name}.\n\nYour {'Student' if user.role == 'student' else 'Instructor'} account has been successfully created. You can now start exploring everything the platform has to offer.\n\nWe're glad to have you with us.",
                )
            if user.role == 'instructor':
                create_instructor_wallet.delay(user.id)
            form.save()
        context = {"form": form}
        return render(request, self.template_name, context)

index_view = IndexView.as_view()


# About View
class AboutView(TemplateView):
    template_name = "core/main/about.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["total_students"] = User.objects.filter(role="student").count()
        context["total_instructors"] = User.objects.filter(role="instructor").count()
        return context

    def post(self, request, *args, **kwargs):
        user_identifier = request.POST.get("user_identifier").strip().lower()
        topic = request.POST.get("topic").strip().title()
        body = request.POST.get("body").strip()

        try:
            user = User.objects.filter(Q(username=user_identifier) | Q(email=user_identifier)).first()
        except User.DoesNotExist:
            return 'This user does not exist'

        if user_identifier and topic and body:
            Report.objects.create(
                user_identifier=user_identifier, topic=topic, body=body
            )
            if user:
                Notification.objects.create(user=user, name=topic, message=body)

        return redirect(about_view_url)

about_view = AboutView.as_view()


# ==================
# USER PROFILE VIEWS
# ==================
class ProfileView(LoginRequiredMixin, DetailView):
    """Public profile display with view tracking"""
    model = User
    template_name = "core/user/main/profile.html"

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        viewer = request.user

        if not request.user.role:
            return redirect(index_view_url)

        if viewer != profile:
            if not profile.views.filter(pk=viewer.pk).exists():
                profile.views.add(viewer)
                Notification.objects.create(
                    user=profile,
                    name="Profile view",
                    message=f"@{viewer.username} just viewed your profile.",
                )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        current_user = request.user

        if user_id:
            user = get_object_or_404(User, pk=int(user_id))
            if current_user not in user.followers.all() and current_user != user:
                user.followers.add(current_user)
            else:
                user.followers.remove(current_user)
        context = {
            'user': user,
        }
        if request.htmx:
            return render(request, "core/user/partials/profile_display.html", context)
        return render(request, self.template_name, context)

profile_view = ProfileView.as_view()


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Profile updating view"""
    model = User
    form_class = UpdateProfileForm
    template_name = "core/user/main/update_profile.html"
    success_url = reverse_lazy(setting_view_url)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

update_profile_view = UpdateProfileView.as_view()


class DescriptionView(LoginRequiredMixin, UpdateView):
    """User description/bio editing"""
    model = User
    form_class = ProfileDescriptionForm
    template_name = "core/user/main/description.html"
    success_url = reverse_lazy(setting_view_url)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

description_view = DescriptionView.as_view()


class SettingsView(LoginRequiredMixin, DetailView):
    """User settings page"""
    model = User
    context_object_name = "user"
    template_name = "core/user/main/settings.html"

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

settings_view = SettingsView.as_view()


class ProfileViewsList(LoginRequiredMixin, DetailView):
    """List of users who viewed profile"""
    model = User
    context_object_name = "profile_user"
    template_name = "core/user/partials/profile_views.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profile = self.get_object()
        context["viewer"] = profile.views.exclude(pk=profile.pk)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

profile_list_views = ProfileViewsList.as_view()


# ==================
# NOTIFICATION VIEWS
# ==================
class NotificationView(LoginRequiredMixin, ListView):
    """User notifications list"""
    model = Notification
    fields = "__all__"
    context_object_name = "notifications"
    template_name = "core/user/main/notification.html"

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get("notification_id")
        user = request.user
        if request.htmx:
            notification = get_object_or_404(Notification, user=user, pk=int(notification_id))
            notification.delete()
            return render(request, "core/user/partials/notification_list.html")
        return redirect(notification_view_url)

notification_view = NotificationView.as_view()


class NotificationDetailView(LoginRequiredMixin, DetailView):
    """Single notification detail"""
    model = Notification
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "notification"
    template_name = "core/user/partials/notification_detail.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        notification = get_object_or_404(
            Notification, pk=self.kwargs.get(self.pk_url_kwarg), user=self.request.user
        )
        if notification and not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return super().get(request, *args, **kwargs)

notification_detail_view = NotificationDetailView.as_view()


# ===================
# SOCIAL VIEWS
# ===================
class DiscoverDeveloperView(LoginRequiredMixin, TemplateView):
    """Search Developers"""
    template_name = "core/user/main/discover_developers.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)

        search = request.GET.get("search")
        user = self.request.user

        if search:
            developers = User.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(username__icontains=search)
            ).exclude(id=user.id)
        else:
            developers = User.objects.exclude(id=user.id)

        context = {"search": search, "developers": developers}

        if request.htmx:
            return render(
                request, "core/user/partials/discover_developers_list.html", context
            )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = int(request.POST.get("user_id"))
        user = request.user
        user_to_follow = get_object_or_404(User, pk=user_id)

        if user in user_to_follow.followers.all():
            user_to_follow.followers.remove(user)
        else:
            user_to_follow.followers.add(user)

        developers = User.objects.exclude(id=user.id)
        context = {'developers': developers}

        if request.htmx:
            return render(request, "core/user/partials/discover_developers_list.html", context)

        return render(request, self.template_name, context)

discover_developer_view = DiscoverDeveloperView.as_view()


# =======================
# INSTRUCTOR WALLET VIEWS
# =======================
class InstructorWalletView(LoginRequiredMixin, DetailView):
    model = Wallet
    fields = "__all__"
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "wallet"
    template_name = "core/user/main/wallet.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        self.object = self.get_object()
        wallet = self.object
        if not user.role or wallet.user.pk != user.pk:
            return redirect(index_view_url)
        return super().get(request, *args, **kwargs)

instructor_wallet_view = InstructorWalletView.as_view()


# ========================
# INSTRUCTOR Courses VIEWS
# ========================
class InstructorCoursesView(LoginRequiredMixin, TemplateView):
    template_name = "core/user/main/instructor_courses.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        search = request.GET.get("search")
        if not user.role and not user.role == 'instructor':
            return redirect(course_view_url)

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


# ====================
# Custom Error Handler
# ====================
def custom_500_view(request):
    return render(request, "core/errors/500.html", status=500)

def custom_404_view(request):
    return render(request, "core/errors/404.html", status=404)