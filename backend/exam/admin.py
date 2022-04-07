from django.contrib import admin

from .models import Student, Module


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ['id', 'email']
        search_fields = ['email']
        ordering = ['email']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ['id', 'short_code', 'name']
        search_fields = ['short_code', 'name']
        ordering = ['short_code']
