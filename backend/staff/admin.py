from django.contrib import admin

from .models import Assessor, Helper
from exam.admin import ExamInline


class AssessorInline(admin.TabularInline):
    model = Assessor.windows.through
    show_change_link = True
    extra = 0


@admin.register(Assessor)
class AssessorAdmin(admin.ModelAdmin):
    list_display = ['email']
    inlines = [ExamInline]


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    list_display = ['email']
