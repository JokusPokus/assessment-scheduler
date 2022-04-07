from django.contrib import admin

from .models import Assessor


class AssessorInline(admin.TabularInline):
    model = Assessor.assessment_phases.through
    show_change_link = True
    extra = 0
