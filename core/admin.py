from django.contrib import admin
from .models import Report
# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user_identifier', 'topic', 'created_at')
    list_filter = ('user_identifier',)
    search_fields = ('user_identifier',)
    fieldsets = (
        ('Report', {'fields': ('user_identifier', 'topic', 'body', 'created_at')}),
    )
    readonly_fields = ('created_at',)