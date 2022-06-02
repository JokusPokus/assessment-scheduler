from django.contrib import admin
from .models import PlanningSheet


class PlanningSheetInline(admin.TabularInline):
    """Admin inline that represents planning sheet instances."""
    model = PlanningSheet
    readonly_fields = ['is_filled_out']
    fields = ['csv', 'is_filled_out']
    show_change_link = True
    extra = 0
