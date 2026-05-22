from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, CourseVideo
from .forms import CreateCourseForm, UpdateCourseForm, CourseVideoForm, UpdateCourseVideoForm
from django.urls import reverse_lazy
from CodeStream.utils import *
from .tasks import *


# ==================
#  Course Index View
# ==================
class CourseIndexView(LoginRequiredMixin, TemplateView):
    template_name = "course/course/course_index.html"

    def dispatch(self, request, *args, **kwargs):
        self.courses = Course.objects.all()
        self.user = request.user

        if not self.user.role:
            return redirect(index_view_url)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search", "")
        if search:
            courses = Course.objects.filter(
                Q(name__icontains=search)
                | Q(instructor__username__icontains=search)
                | Q(description__icontains=search)
            ).exclude(published=False).distinct()
        else:
            courses = self.courses.exclude(published=False).distinct()

        context = {"courses": courses, "search": search}

        if request.htmx:
            return render(request, "course/course/partials/courses_list.html", context)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course_delete = request.POST.get("course_delete_id")
        course_like = request.POST.get("course_like_id")

        context = {
            'courses': self.courses,
        }

        # Action for deleting course
        if course_delete:
            course = get_object_or_404(Course, id=int(course_delete))
            if self.user == course.instructor:
                course.delete()
            if request.htmx:
                return render(request, "course/course/partials/courses_list.html", context)

        # Action for liking the course
        if course_like:
            course = get_object_or_404(Course, id=int(course_like))
            if self.user not in course.likes.all():
                course.likes.add(self.user)
            else:
                course.likes.remove(self.user)
            if request.htmx:
                return render(request, "course/course/partials/courses_list.html", context)
        return render(request, self.template_name, context)


course_index_view = CourseIndexView.as_view()


# ===================
#  Course Detail View
# ===================
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "course/course/course_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.course = get_object_or_404(Course, id =self.kwargs["pk"])
        self.videos = self.course.course_videos()
        self.active_video = self.videos.first() if self.videos.exists() else None

        if not self.user.role:
            return redirect(course_view_url)

        return super().dispatch(request, *args, **kwargs)

    def get_shared_context(self):
        return {
            'course': self.course,
            'videos': self.videos,
            'active_video': self.active_video,
        }

    def get(self, request, *args, **kwargs):

        if self.user not in self.course.views.all() and self.user != self.course.instructor:
            self.course.views.add(self.user)

        return render(request, self.template_name, self.get_shared_context())

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        video_id = request.POST.get("video_id")

        # Access: Course Instructor (Toggle Course Published Status)
        if course_id and self.user == self.course.instructor:
            self.course.published = not self.course.published
            self.course.save(update_fields=["published"])
            if request.htmx:
                return render(request, self.template_name, self.get_shared_context())
        # Access: Course Instructor (Delete Course Videos)
        if video_id and self.user == self.course.instructor:
            if request.htmx:
                try:
                    course_video =self.videos.get(pk=int(video_id))
                except self.videos.DoesNotExist:
                    return render(request, self.template_name, self.get_shared_context())

                course_video.delete()
                return render(request, "course/course/partials/course_videos_list.html", self.get_shared_context())

        return render(request, self.template_name, self.get_shared_context())

course_detail_view = CourseDetailView.as_view()


# ========================================
#  Create Course View (Access: Instructor)
# ========================================
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
        course = form.save(commit=False)
        course.instructor = self.request.user
        course.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(create_course_done_view_url, kwargs={"pk": self.object.pk})

create_course_view = CreateCourseView.as_view()


# ====================================================
#  Create Course Done View (Access: Course Instructor)
# ====================================================
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


# ===============================================
#  Update Course View (Access: Course Instructor)
# ===============================================
class UpdateCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = UpdateCourseForm
    context_object_name = 'course'
    template_name = "course/course/update_course.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if user.role != "instructor" or not user.role or user != obj.instructor:
            return redirect(course_view_url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(update_course_done_view_url, kwargs={"pk": self.object.pk})

update_course_view = UpdateCourseView.as_view()


# ====================================================
#  Update Course Done View (Access: Course Instructor)
# ====================================================
class UpdateCourseDoneView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "course/course/update_course_done.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if user.role != "instructor" or not user.role or user != obj.instructor:
            return redirect(create_course_view_url)
        return super().get(request, *args, **kwargs)

update_course_done_view = UpdateCourseDoneView.as_view()


# ==============================================
#  Course Info View (Access: Authenticated User)
# ==============================================
class CourseInfoView(LoginRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "pk"
    pk_field = "pk"
    template_name = "course/course/partials/course_info.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        self.object = self.get_object()
        course = self.object
        enrolled_student = request.GET.get("enrolled_student")

        if not user.role:
            return redirect(course_view_url)


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


# =====================================================
#  Create Course Video View (Access: Course Instructor)
# =====================================================
class CreateCourseVideoView(LoginRequiredMixin, TemplateView):
    template_name = "course/course/create_course_video.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs['course_id'])

        if request.user.role != 'instructor' or request.user != self.course.instructor:
            return redirect(self.course.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CourseVideoForm()
        context = {
            "course": self.course,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CourseVideoForm(request.POST, request.FILES)

        if form.is_valid():
            course_video = form.save(commit=False)
            course_video.course = self.course
            course_video.save()

            video_url = course_video.video.url

            clip = VideoFileClip(video_url)
            duration = int(clip.duration)

            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60

            # Save the Course Duration
            course_video.duration = duration
            course_video.formatted_duration = f'{hours:02}:{minutes:02}:{seconds:02}'
            course_video.save()

            # Trigger Celery asynchronous tasks
            generate_thumbnail_task.delay(course_video.id)
            send_user_notification_task.delay(course_video.id)

            return redirect(self.course.get_absolute_url())

        context = {
            "course": self.course,
            "form": form,
        }

        return render(request, self.template_name, context)

create_course_video_view = CreateCourseVideoView.as_view()


# =====================================================
#  Update Course Video View (Access: Course Instructor)
# =====================================================
class UpdateCourseVideoView(LoginRequiredMixin, UpdateView):
    model = CourseVideo
    form_class = UpdateCourseVideoForm
    pk_url_kwarg = 'pk'
    pk_field = "pk"
    context_object_name = "course_video"
    template_name = "course/course/update_course_video.html"

    def dispatch(self, request, *args, **kwargs):
        self.course_video = get_object_or_404(CourseVideo, id=self.kwargs.get('pk'))
        self.user = request.user
        if not self.user.role or self.user.role != "instructor" or self.user != self.course_video.course.instructor:
            return redirect(self.course_video.course.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        video_form = form.save(commit=False)
        if self.user == self.course_video.course.instructor:
            video_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("course-detail-view", kwargs={"pk": self.course_video.course.pk})

update_course_video_view = UpdateCourseVideoView.as_view()