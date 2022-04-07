from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ['id', 'email']
        search_fields = ['email']
        ordering = ['email']
