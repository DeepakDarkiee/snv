from django.contrib import admin

from .models import *

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "email",
        "contact",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "email",
        "contact",
        "created_at",
        "updated_at",
    )
