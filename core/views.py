from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.models import User, Notification, Wallet
from django.db.models import Q
from .models import Report
from .forms import UserRoleForm
from course.models import Course
import time
# Create your views here.


# Landing Page View
class IndexView(TemplateView):
  template_name = "core/html/index.html"

  def get(self, request, *args, **kwargs):
    form = UserRoleForm()
    instructors = User.objects.filter(role='instructor').order_by('-last_login')
    search = request.GET.get('search')
    
    if search:
      time.sleep(2)
      courses = Course.objects.filter(Q(name__icontains=search)).order_by('-created_at')
    else:
      courses = Course.objects.order_by('-created_at')
      
    context = {"form": form, 'instructors':instructors, 'courses': courses}
    
    if request.htmx:
      return render(request, 'core/partials/index_content.html', context)
  
    return render(request, self.template_name, context)

  def post(self, request, *args, **kwargs):
    user = request.user
    form = UserRoleForm(request.POST, instance=user)
    if form.is_valid():
      if user.role:
        Notification.objects.create(
          user=user,
          title="Welcome New User",
          message=f"Congratulations you have an account with Code Stream as {'Student' if user.role == 'student' else 'Instructor'}",
        )
      if user.role == "instructor":
        Wallet.objects.create(user=user)
      form.save()
    context = {"form": form}
    return render(request, self.template_name, context)


# About View
class AboutView(TemplateView):
  template_name = "core/html/about.html"

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context["total_students"] = User.objects.filter(role="student").count()
    context["total_instructors"] = User.objects.filter(role="instructor").count()
    return context

  def post(self, request, *args, **kwargs):
    user_identifier = request.POST.get("user_identifier", "").strip().lower()
    topic = request.POST.get("topic", "").strip().title()
    body = request.POST.get("body", "").strip()

    user = User.objects.filter(
      Q(username__iexact=user_identifier) | Q(email__iexact=user_identifier)
    ).first()

    if user_identifier and topic and body:
      Report.objects.create(user_identifier=user_identifier, topic=topic, body=body)
      if user:
        Notification.objects.create(user=user, title=topic, message=body)

    return redirect("core:about-view")
