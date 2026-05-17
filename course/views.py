from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Course, CourseVideo,
)
from .forms import CreateCourseForm, UpdateCourseForm, CourseVideoForm
from django.urls import reverse_lazy
from CodeStream.utils import index_view_url, course_view_url, create_course_view_url


class CourseView(LoginRequiredMixin, TemplateView):
    """Main course landing page."""
    template_name = "course/course/course_index.html"

    def get(self, request, *args, **kwargs):
        if not request.user.role:
            return redirect(index_view_url)
        search = request.GET.get("search", "")
        if search:
            courses = Course.objects.filter(
                Q(name__icontains=search)
                | Q(instructor__username__icontains=search)
                | Q(description__icontains=search)
            )
        else:
            courses = Course.objects.all()

        context = {"courses": courses, "search": search}

        if request.htmx:
            return render(request, "course/course/partials/courses_list.html", context)

        return render(request, self.template_name, context)

course_view = CourseView.as_view()


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "course/course/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        videos = course.course_videos()
        course_video_form = CourseVideoForm()

        context["videos"] = videos
        context["active_video"] = videos.first() if videos.exists() else None
        context["form"] = kwargs.get("form", course_video_form)
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.role:
            return redirect(index_view_url)
        delete_id = request.GET.get("course_id")
        course_video = get_object_or_404(CourseVideo, pk=delete_id)
        course = get_object_or_404(Course, pk=course_video.course.pk)
        print(f'This is the name of the course: {course_video.name}')
        print(f'This is the Delete Id of this Video: {delete_id}  \nThe Data Type is:{type(delete_id)}')
        if course.instructor != user:
            course_video.delete()
        return redirect(request.META.get("HTTP_REFERER"))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        course = self.object
        form = CourseVideoForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            return redirect(course.get_absolute_url())

            # If invalid, re-render with form errors and all context
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

course_detail_view = CourseDetailView.as_view()


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = "course/course/create_course.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role != "instructor" or not user.role:
            return redirect(course_view_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.instructor = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("course:create-course-done", kwargs={"pk": self.object.pk})

create_course_view = CreateCourseView.as_view()


class CreateCourseDoneView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "course/course/create_course_done.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if user.role != "instructor" or not user.role or user != obj.instructor:
            return redirect(create_course_view_url)
        return super().get(request, *args, **kwargs)

create_course_done_view = CreateCourseDoneView.as_view()


class UpdateCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = UpdateCourseForm
    template_name = "course/course/update_course.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if user.role != "instructor" or not user.role or user != obj.instructor:
            return redirect(course_view_url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("course:create-course-done", kwargs={"pk": self.object.pk})

update_course_view = UpdateCourseView.as_view()


class CourseInfoView(LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "pk"
    pk_field = "pk"
    template_name = "course/course/partials/course_info.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.role:
            return redirect(course_view_url)

        self.object = self.get_object()
        course = self.object
        enrolled_student = request.GET.get("enrolled_student")

        if enrolled_student:
            students = course.students.filter(
                Q(username__icontains=enrolled_student)
                | Q(first_name__icontains=enrolled_student)
                | Q(last_name__icontains=enrolled_student)
            )
        else:
            students = course.students.all()
        context = {
            "course": course,
            "students": students,
            "enrolled_student": enrolled_student,
        }

        if request.htmx:
            return render(
                request,
                "course/course/partials/course_info_enrolled_student.html",
                context,
            )

        return render(request, self.template_name, context)

course_info_view = CourseInfoView.as_view()
