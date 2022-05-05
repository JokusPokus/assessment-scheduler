from django.contrib import admin

from .models import Student, Module, Exam


class ExamInline(admin.TabularInline):
    model = Exam
    fields = ['id', 'module', 'student']
    read_only_fields = ['length']
    show_change_link = True
    extra = 0

    @staticmethod
    def length(obj):
        return obj.length


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    search_fields = ['email']
    ordering = ['email']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'name',
        'standard_length',
        'alternative_length'
    ]
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'module',
        'style',
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
        'helper__email'
    ]
    ordering = ['module__code']
