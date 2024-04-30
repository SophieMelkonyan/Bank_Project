# from django.contrib import admin
# from .models import User
#
# admin.site.register(User)


from django.contrib import admin
from .views import User
from .views import Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    search_fields = ("first_name", "last_name",)
    readonly_fields = ("email", "created_at",)
    fieldsets = (
        (
            "GENERAL",
            {"fields": ("email", "password", "first_name", "last_name", )},
        ),
        (
            "INFO",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",

                )
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user",)
    readonly_fields = ("card_number", "bank_account", "card_account", "pin_code")
    fieldsets = (
        (
            "GENERAL",
            {"fields": ("balance", "bank")},
        ),
        (

            "INFO",
            {"fields": ("card_number", "bank_account", "card_account", "pin_code")}
        )

    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
