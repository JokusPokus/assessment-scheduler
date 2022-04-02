from django.contrib import admin
from .models import AssessmentPhase, Window


class WindowInline(admin.TabularInline):
    model = Window
    fields = ['position', 'start_date', 'end_date', 'block_length']
    show_change_link = True
    extra = 0


@admin.register(AssessmentPhase)
class AssessmentPhaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'semester', 'category', 'room_limit']
    search_fields = ['semester', 'year', 'category']
    ordering = ['-year']
    inlines = [WindowInline]
