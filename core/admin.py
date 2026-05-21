from django.contrib import admin
from django.utils.html import format_html
from .models import ShortVideo, Report


# =================
# SHORT VIDEO ADMIN
# =================
@admin.register(ShortVideo)
class ShortVideoAdmin(admin.ModelAdmin):

    list_display = (
        'thumbnail_preview',
        'name',
        'user',
        'created_at',
    )

    list_filter = (
        'created_at',
        'user',
    )

    search_fields = (
        'name',
        'user__username',
    )

    readonly_fields = (
        'slug',
        'thumbnail_preview_large',
        'video_preview',
        'created_at',
        'updated_at',
    )


    fieldsets = (
        ("Video Info", {
            'fields': (
                'user',
                'name',
                'slug',
                'description',
            )
        }),

        ("Media", {
            'fields': (
                'video',
                'video_preview',
                'thumbnail',
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
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px;" />',
                obj.thumbnail.url
            )
        return "No Thumbnail"

    def thumbnail_preview_large(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="250" style="border-radius:10px;" />',
                obj.thumbnail.url
            )
        return "No Thumbnail"

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="300" controls>'
                '<source src="{}" type="video/mp4">'
                '</video>',
                obj.video.url
            )
        return "No Video"


# =================
# SHORT VIDEO ADMIN
# =================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user_identifier', 'topic', 'created_at')
    list_filter = ('user_identifier',)
    search_fields = ('user_identifier',)
    fieldsets = (
        ('Report', {'fields': ('user_identifier', 'topic', 'body', 'created_at')}),
    )
    readonly_fields = ('created_at',)