from django.contrib import admin

from .models import User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "contact",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "contact",
        "created_at",
        "updated_at",
    )
