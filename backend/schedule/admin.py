from django.contrib import admin

from .models import AssessmentPhase, Window
from input.admin import PlanningSheetInline
from staff.admin import AssessorInline


class WindowInline(admin.TabularInline):
    model = Window
    fields = ['position', 'start_date', 'end_date', 'block_length']
    show_change_link = True
    extra = 0


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    list_display = [
        'assessment_phase',
        'position',
        'start_date',
        'end_date',
        'block_length'
    ]
    ordering = ['assessment_phase', 'position']
    inlines = [PlanningSheetInline]


@admin.register(AssessmentPhase)
class AssessmentPhaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'semester', 'category', 'room_limit']
    search_fields = ['semester', 'year', 'category']
    ordering = ['-year']
    inlines = [WindowInline, AssessorInline]
