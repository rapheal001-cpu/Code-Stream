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

course_index_view = CourseIndexView.as_view()


# ===================================
#  Course Action (Delete And Like View)
# ===================================
class CourseActionDeleteAndLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        course_delete = request.POST.get("course_delete_id")
        course_like = request.POST.get("course_like_id")
        user = request.user
        courses = Course.objects.all()

        # Only Authenticated User
        if not user.role:
            return redirect(course_index_view)

        context = {
            'courses': courses,
        }

        # Action for deleting course
        if course_delete:
            course = get_object_or_404(Course, id=int(course_delete))
            if user == course.instructor:
                course.delete()
            if request.htmx:
                return render(request, "course/course/partials/courses_list.html", context)

        # Action for liking the course
        if course_like:
            course = get_object_or_404(Course, id=int(course_like))
            if user not in course.likes.all():
                course.likes.add(user)
            else:
                course.likes.remove(user)
            if request.htmx:
                return render(request, "course/course/partials/courses_list.html", context)
        return render(request, "course/course/course_index.html", context)

course_action_delete_and_like_view = CourseActionDeleteAndLikeView.as_view()


# ===================
#  Course Detail View
# ===================
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "course/course/course_detail.html"

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        videos = course.course_videos()
        active_video = videos.first() if videos.exists() else None
        user = request.user

        if user not in course.views.all() and user != course.instructor:
            course.views.add(user)

        context = {
            'course': course,
            'videos': videos,
            'active_video': active_video,
        }
        return render(request, self.template_name, context)

course_detail_view = CourseDetailView.as_view()


# =======================================================================
#  Course Video Action By The Course Instructor (Course Video Delete View)
# =======================================================================
class CourseVideoActionDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        video_id = request.POST.get("video_id")
        course_id = request.POST.get("course_id")
        course = get_object_or_404(Course, id=int(course_id))
        videos = course.course_videos()
        course_video = get_object_or_404(CourseVideo, id=int(video_id))

        context = {
            'videos': videos,
            'course': course,
        }

        if user == course_video.course.instructor:
            course_video.delete()
            if request.htmx:
                return render(request, "course/course/partials/course_videos_list.html", context)
        else:
            return redirect(course_view_url)

        return render(request, "course/course/course_detail.html", context)

course_video_action_delete_view = CourseVideoActionDeleteView.as_view()


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
    template_name = "course/course/update_course_video.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        course_video = self.object
        user = request.user
        if not user.role or user.role != "instructor" or user != course_video.course.instructor:
            return redirect(course_video.course.get_absolute_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        course_video = form.save(commit=False)
        if self.request.user == course_video.course.instructor:
            form.save()
        return super().form_valid(form)

update_course_video_view = UpdateCourseVideoView.as_view()