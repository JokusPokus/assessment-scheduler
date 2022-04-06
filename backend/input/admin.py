from django.contrib import admin
from .models import PlanningSheet


class PlanningSheetInline(admin.TabularInline):
    model = PlanningSheet
    fields = ['csv']
    show_change_link = True
    extra = 0
