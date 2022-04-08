from django.contrib import admin

from .models import Student, Module, Exam


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    search_fields = ['email']
    ordering = ['email']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'module',
        'assessor',
        'student',
        'helper',
    ]
    search_fields = [
        'code',
        'module__name',
        'module__code',
        'assessor__email',
        'student__email',
        'assistant__email'
    ]
    ordering = ['module__code']
