from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
  Course,
  #   CourseVideo,
)
from .forms import CreateCourseForm, UpdateCourseForm, CourseVideoForm
from django.urls import reverse_lazy


class CourseView(LoginRequiredMixin, TemplateView):
  """Main course landing page."""

  template_name = "course/course/course_index.html"

  def get(self, request, *args, **kwargs):
    if not request.user.role:
      return redirect("core:index-view")

    search = request.GET.get("search", "").strip()
    if search:
      courses = Course.objects.filter(Q(name__icontains=search) | Q(instructor__username__icontains=search) | Q(description__icontains=search))
    else:
      courses = Course.objects.all()

    context = {"courses": courses, "search": search}
    
    if request.htmx:
      return render(request, 'course/course/partials/courses_list.html', context)

    return render(request, self.template_name, context)


class CourseDetailView(LoginRequiredMixin, DetailView):
  model = Course
  slug_field = "slug"
  slug_url_kwarg = "slug"
  template_name = "course/course/course_detail.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    course = self.object
    videos = course.videos.all()
        
    context["videos"] = videos
    context["active_video"] = videos.first() if videos.exists() else None
    context["form"] = kwargs.get("form", CourseVideoForm())
    return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    course = self.object
    form = CourseVideoForm(request.POST, request.FILES)
        
    if form.is_valid():
      video = form.save(commit=False)
      video.course = course
      video.save()
      # Redirect after successful POST (PRG pattern)
      return redirect(course.get_absolute_url())
        
      # If invalid, re-render with form errors and all context
    context = self.get_context_data(form=form)
    return render(request, self.template_name, context)


class CreateCourseView(LoginRequiredMixin, CreateView):
  model = Course
  form_class = CreateCourseForm
  template_name = "course/course/create_course.html"
  
  def get(self, request, *args, **kwargs):
    user = request.user
    if user.role != 'instructor' or not user.role:
      return redirect('course:course-index')
    return super().get(request, *args, **kwargs)
  
  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.instructor = self.request.user
    obj.save()
    return super().form_valid(form)

  def get_success_url(self):
    return reverse_lazy('course:create-course-done', kwargs={'slug': self.object.slug})


class CreateCourseDoneView(LoginRequiredMixin, DetailView):
  model = Course
  slug_field = 'slug'
  slug_url_kwarg = 'slug'
  context_object_name = 'course'
  template_name = "course/course/create_course_done.html"
  
  def get(self, request, *args, **kwargs):
    obj = self.get_object()
    user = request.user
    if user.role != 'instructor' or not user.role or user != obj.instructor:
      return redirect('course:create-course')
    return super().get(request, *args, **kwargs)


class UpdateCourseView(LoginRequiredMixin, UpdateView):
  model = Course
  form_class = UpdateCourseForm
  template_name = "course/course/update_course.html"
  
  def get(self, request, *args, **kwargs):
    user = request.user
    obj = self.get_object()
    print(obj.instructor.username)
    print(obj.name)
    if user.role != 'instructor' or not user.role or user != obj.instructor:
      return redirect('course:course-index')
    return super().get(request, *args, **kwargs)

  def get_success_url(self):
    return reverse_lazy('course:create-course-done', kwargs={'slug': self.object.slug})


class CourseInfoView(LoginRequiredMixin, DetailView):
  model = Course
  slug_url_kwarg = 'slug'
  slug_field = 'slug'
  template_name = "course/course/partials/course_info.html"
  
  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    course = self.object
    enrolled_student = request.GET.get('enrolled_student')
    
    if enrolled_student:
      students = course.students.filter(Q(username__icontains=enrolled_student) | Q(first_name__icontains=enrolled_student) | Q(last_name__icontains=enrolled_student))
    else:
      students = course.students.all()
    context = {
      'course': course,
      'students': students,
      'enrolled_student': enrolled_student,
    }
    
    if request.htmx:
      return render(request, 'course/course/partials/course_info_enrolled_student.html', context)
      
    return render(request, self.template_name, context)