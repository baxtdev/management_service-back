from django.contrib import admin

# Register your models here.

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'created_at')
    readonly_fields = ('file', 'created_at')
