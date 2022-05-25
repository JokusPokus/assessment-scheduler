from django.contrib import admin

from .models import (
    AssessmentPhase,
    Window,
    BlockSlot,
    BlockTemplate,
    Block,
    Schedule,
)
from input.admin import PlanningSheetInline
from staff.admin import AssessorInline


class WindowInline(admin.TabularInline):
    model = Window
    fields = ['position', 'start_date', 'end_date', 'block_length']
    show_change_link = True
    extra = 0


class BlockSlotInline(admin.TabularInline):
    model = BlockSlot
    fields = ['start_time']
    extra = 0


class BlockTemplateInline(admin.TabularInline):
    model = Window.block_templates.through
    show_change_link = True
    extra = 0


class BlockInline(admin.TabularInline):
    model = Block
    fields = ['block_slot', 'template']
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
    inlines = [
        BlockSlotInline,
        PlanningSheetInline,
        BlockTemplateInline,
        AssessorInline
    ]


@admin.register(AssessmentPhase)
class AssessmentPhaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'semester', 'category', 'room_limit']
    search_fields = ['semester', 'year', 'category']
    ordering = ['-year']
    inlines = [WindowInline]


@admin.register(BlockTemplate)
class BlockTemplateAdmin(admin.ModelAdmin):
    list_display = ['block_length', 'exam_length', 'exam_start_times']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'window', 'phase']
    inlines = [BlockInline]

    @staticmethod
    def phase(obj):
        return str(obj.window.assessment_phase)
