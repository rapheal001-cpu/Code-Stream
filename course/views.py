from CodeStream.views import RoleRequiredMixin, InstructorRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from moviepy import VideoFileClip
from .models import Course
from .forms import CourseForm, UpdateCourseForm, CourseVideoForm, UpdateCourseVideoForm
from django.urls import reverse_lazy, reverse
from CodeStream.utils import *
from .tasks import *


# ==================
#  Course Index View
# ==================
class CourseIndexView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "course/course/course_index.html"

    def dispatch(self, request, *args, **kwargs):
        self.courses = Course.objects.exclude(published=False)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        if search:
            courses = Course.objects.filter(
                Q(name__icontains=search)
                | Q(instructor__username__icontains=search)
                | Q(description__icontains=search)
            )
        else:
            courses = self.courses

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
class CourseDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    template_name = "course/course/course_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.course = get_object_or_404(Course, id =self.kwargs["pk"])
        self.videos = self.course.course_videos()
        self.active_video = self.videos.first() if self.videos.exists() else None

        return super().dispatch(request, *args, **kwargs)

    def get_shared_context(self, active_video):
        return {
            'course': self.course,
            'videos': self.videos,
            'active_video': active_video,
        }

    def get(self, request, *args, **kwargs):
        if self.user not in self.course.views.all() and self.user != self.course.instructor:
            self.course.views.add(self.user)
        return render(request, self.template_name, self.get_shared_context(self.active_video))

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")
        video_id = request.POST.get("video_id")
        select_active_video_id = request.POST.get("select_active_video_id")

        # Access: Course Instructor (Toggle Course Published Status)
        if course_id and self.user == self.course.instructor:
            self.course.published = not self.course.published
            self.course.save(update_fields=["published"])
            if request.htmx:
                return render(request, self.template_name, self.get_shared_context(self.active_video))

        # Access: Course Instructor (Delete Course Videos)
        if video_id and self.user == self.course.instructor:
            if request.htmx:
                try:
                    course_video =self.videos.get(pk=int(video_id))
                except self.videos.DoesNotExist:
                    return render(request, self.template_name, self.get_shared_context(self.active_video))

                course_video.delete()
                return render(request, "course/course/partials/course_videos_list.html", self.get_shared_context(self.active_video))

        # Access: Authenticated User (Select A video to become the active video)
        if select_active_video_id:
            active_video = self.course.videos.filter(id=int(select_active_video_id)).first()
            if request.htmx:
                return render(request, self.template_name, self.get_shared_context(active_video))

        return render(request, self.template_name, self.get_shared_context(active_video))

course_detail_view = CourseDetailView.as_view()


# ========================================
#  Create Course View (Access: Instructor)
# ========================================
class CreateCourseView(LoginRequiredMixin, InstructorRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "course/course/create_course.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        name = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        thumbnail = form.cleaned_data.get("thumbnail")
        price = form.cleaned_data.get("price")
        youtube_link = form.cleaned_data.get("youtube_link")
        github_link = form.cleaned_data.get("github_link")
        is_paid = form.cleaned_data.get("is_paid")
        # Celery Handle This
        process_course_creation_task.delay(self.user, name, description, thumbnail, price, youtube_link, github_link, is_paid)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(create_course_done_view_url, kwargs={"pk": self.object.pk})

create_course_view = CreateCourseView.as_view()


# ====================================================
#  Create Course Done View (Access: Course Instructor)
# ====================================================
class CreateCourseDoneView(LoginRequiredMixin, InstructorRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "course/course/create_course_done.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.user = request.user
        if self.user != self.object.instructor:
            return redirect(course_view_url)
        return super().dispatch(request, *args, **kwargs)

create_course_done_view = CreateCourseDoneView.as_view()


# ===============================================
#  Update Course View (Access: Course Instructor)
# ===============================================
class UpdateCourseView(LoginRequiredMixin, InstructorRequiredMixin, UpdateView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    form_class = UpdateCourseForm
    context_object_name = 'course'
    template_name = "course/course/update_course.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = self.get_object()
        self.user = request.user
        if self.user != self.course.instructor:
            return redirect(course_view_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)

        name = form.cleaned_data.get('name')
        thumbnail = form.cleaned_data.get('thumbnail')
        description = form.cleaned_data.get('description')
        youtube_link = form.cleaned_data.get('youtube_link')
        github_link = form.cleaned_data.get('github_link')
        # Celery Handle Update Course
        process_update_course_task.delay(self.course.id, self.user, name, thumbnail, description, youtube_link, github_link)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(update_course_done_view_url, kwargs={"pk": self.object.pk})

update_course_view = UpdateCourseView.as_view()


# ====================================================
#  Update Course Done View (Access: Course Instructor)
# ====================================================
class UpdateCourseDoneView(LoginRequiredMixin, InstructorRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "course/course/update_course_done.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.user = request.user
        if not self.user.is_authenticated or self.user != self.object.instructor:
            return redirect(course_view_url)
        return super().dispatch(request, *args, **kwargs)

update_course_done_view = UpdateCourseDoneView.as_view()


# ==============================================
#  Course Info View (Access: Authenticated User)
# ==============================================
class CourseInfoView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Course
    pk_url_kwarg = "pk"
    pk_field = "pk"
    template_name = "course/course/partials/course_info.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.user = request.user

        if not self.user.is_authenticated or not self.user.role:
            return redirect(login_view_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        enrolled_student = request.GET.get("enrolled_student")

        if enrolled_student:
            students = self.object.students.filter(
                Q(username__icontains=enrolled_student)
                | Q(first_name__icontains=enrolled_student)
                | Q(last_name__icontains=enrolled_student)
            )
        else:
            students = self.object.students.all()
        context = {
            "course": self.object,
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
class CreateCourseVideoView(LoginRequiredMixin, InstructorRequiredMixin, FormView):
    model = CourseVideo
    form_class = CourseVideoForm
    template_name = "course/course/create_course_video.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs['course_id'])
        self.user = request.user

        if self.user != self.course.instructor:
            return redirect(self.course.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        name = form.cleaned_data.get('name')

        return super().form_valid(form)


    def post(self, request, *args, **kwargs):
        form = CourseVideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            name = form.cleaned_data.get('name')

            # Celery Process Course Video Task
            process_course_video_task.delay()
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

        return render(request, self.template_name, self.get_shared_context(form))

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
        self.course_video = self.get_object()
        self.course = self.course_video.course
        self.user = request.user

        if not self.user.is_authenticated or self.user != self.course.instructor:
            return redirect(self.course.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        video_form = form.save(commit=False)
        if self.user == self.course.instructor:
            video_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("course-detail-view", kwargs={"pk": self.course.pk})

update_course_video_view = UpdateCourseVideoView.as_view()



class InstructorCoursesView(LoginRequiredMixin, TemplateView):
    template_name = "course/course/instructor_courses.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.courses = Course.objects.filter(instructor=self.user)


        if self.user.role != 'instructor':
            return redirect(course_view_url)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")

        if search:
            courses = self.courses.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        else:
            courses = self.courses

        context = {
            "courses": courses,
            "search": search,
        }

        if request.htmx:
            return render(request, "course/course/partials/my_courses_list.html", context)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get("course_id")

        context = {
            'courses': self.courses,
        }

        # Access: Course Instructor (Toggle Course Published Status)
        if course_id:
            try:
                course = self.courses.get(pk=int(course_id))
                course.published = not course.published
                course.save(update_fields=['published'])
            except Course.DoesNotExist:
                return render(request, 'course/course/partials/my_courses_list.html', context)

            if request.htmx:
                return render(request, 'course/course/partials/my_courses_list.html', context)


instructor_courses_view = InstructorCoursesView.as_view()
