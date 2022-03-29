from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from .models import User, Organization


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    list_display = ["id", "email", "date_joined", "organization"]
    search_fields = ["email", "organization"]
    ordering = ["id"]

    fieldsets = (
        *OriginalUserAdmin.fieldsets,
        (None, {'fields': ['organization']},),
    )
