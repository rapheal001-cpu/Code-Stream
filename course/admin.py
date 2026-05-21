from django.contrib import admin
from django.utils.html import format_html
from .models import Course, CourseVideo, Enrollment


# =========================
# INLINE MODELS
# =========================

class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 0
    fields = (
        'name',
        'formatted_duration',
        'video_preview',
        'thumbnail_preview',
        'created_at',
    )
    readonly_fields = (
        'video_preview',
        'thumbnail_preview',
        'created_at',
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px;" />',
                obj.thumbnail.url
            )
        return "No Thumbnail"

    thumbnail_preview.short_description = "Thumbnail"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="220" controls>'
                '<source src="{}" type="video/mp4">'
                '</video>',
                obj.video.url
            )
        return "No Video"

    video_preview.short_description = "Preview"


# =========================
# COURSE ADMIN
# =========================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'thumbnail_preview',
        'name',
        'instructor',
        'price',
        'total_students',
        'total_videos',
        'total_views',
        'total_likes',
        'created_at',
    )

    list_filter = (
        'created_at',
        'updated_at',
        'instructor',
    )

    search_fields = (
        'name',
        'description',
        'instructor__username',
        'instructor__email',
    )

    readonly_fields = (
        'slug',
        'created_at',
        'updated_at',
        'thumbnail_preview_large',
        'analytics',
    )

    ordering = ('-created_at',)

    inlines = [CourseVideoInline]

    fieldsets = (
        ("Course Information", {
            'fields': (
                'instructor',
                'name',
                'slug',
                'description',
                'price',
            )
        }),

        ("Thumbnail", {
            'fields': (
                'thumbnail',
                'thumbnail_preview_large',
            )
        }),

        ("Analytics", {
            'fields': (
                'analytics',
            )
        }),

        ("Dates", {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    # =========================
    # CUSTOM METHODS
    # =========================

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="70" height="50" style="border-radius:8px;" />',
                obj.thumbnail.url
            )
        return "No Image"

    thumbnail_preview.short_description = "Thumbnail"

    def thumbnail_preview_large(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="300" style="border-radius:12px;" />',
                obj.thumbnail.url
            )
        return "No Image"

    thumbnail_preview_large.short_description = "Preview"

    def analytics(self, obj):
        return format_html(
            """
            <div style="padding:15px;">
                <h3>Course Analytics</h3>
                <p><strong>Total Students:</strong> {}</p>
                <p><strong>Total Videos:</strong> {}</p>
                <p><strong>Total Views:</strong> {}</p>
                <p><strong>Total Likes:</strong> {}</p>
                <p><strong>Total Duration:</strong> {}</p>
            </div>
            """,
            obj.total_students,
            obj.total_videos,
            obj.total_views,
            obj.total_likes,
            obj.total_videos_duration,
        )

    analytics.short_description = "Statistics"


# =========================
# COURSE VIDEO ADMIN
# =========================

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):

    list_display = (
        'thumbnail_preview',
        'name',
        'course',
        'formatted_duration',
        'created_at',
    )

    list_filter = (
        'created_at',
        'course',
    )

    search_fields = (
        'name',
        'course__name',
    )

    readonly_fields = (
        'thumbnail_preview_large',
        'video_preview',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ("Video Information", {
            'fields': (
                'course',
                'name',
                'description',
                'duration',
                'formatted_duration',
            )
        }),

        ("Media", {
            'fields': (
                'video',
                'video_preview',
                'thumbnail',
                'thumbnail_url',
                'thumbnail_preview_large',
            )
        }),

        ("Dates", {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail or obj.thumbnail_url:
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px;" />',
                obj.thumbnail.url if obj.thumbnail.url else obj.thumbnail_url
            )
        return "No Thumbnail"

    def thumbnail_preview_large(self, obj):
        if obj.thumbnail or obj.thumbnail_url:
            return format_html(
                '<img src="{}" width="250" style="border-radius:10px;" />',
                obj.thumbnail.url if obj.thumbnail.url else obj.thumbnail_url
            )
        return "No Thumbnail"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="350" controls>'
                '<source src="{}" type="video/mp4">'
                '</video>',
                obj.video.url
            )
        return "No Video"


# =========================
# ENROLLMENT ADMIN
# =========================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'course',
        'amount_paid',
        'is_paid',
        'enrolled_at',
    )

    list_filter = (
        'is_paid',
        'enrolled_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'course__name',
    )

    autocomplete_fields = (
        'user',
        'course',
    )

    readonly_fields = (
        'enrolled_at',
    )

    fieldsets = (
        ("Enrollment", {
            'fields': (
                'user',
                'user_preview_avatar',
                'course__name',

            )
        })
    )

    def user_preview_avatar(self, obj):
        if obj.user.avatar:
            return format_html(
                '<img src="{}" width="250" style="border-radius:10px;" />',
                obj.user.avatar.url
            )
        return "No Avatar"