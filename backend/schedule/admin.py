from django.contrib import admin
from django.utils.html import format_html

from .models import (
    AssessmentPhase,
    Window,
    BlockSlot,
    BlockTemplate,
    Block,
    Schedule,
)
from exam.models import Exam
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
    readonly_fields = ['exams']
    fields = ['block_slot', 'template', 'exams']
    show_change_link = True
    extra = 0

    @admin.display(description='Exams scheduled')
    def exams(self, obj):
        exams = Exam.objects.filter(
            time_slot__in=obj.exam_slots.all()
        )
        return format_html(
            "<br>".join(
                [
                    f"{exam.time_slot.start_time.strftime('%Y-%m-%d, %H:%M')}: "
                    f"{exam.module.code} | {exam.student.email}"
                    for exam in exams
                ]
            )
        )


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
    readonly_fields = ['penalty']
    inlines = [BlockInline]

    @staticmethod
    def phase(obj):
        return str(obj.window.assessment_phase)
