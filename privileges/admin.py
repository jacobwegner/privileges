from django.contrib import admin

from privileges.models import Grant, Privilege

from django.contrib.auth import get_user_model

User = get_user_model()
username_field = User.USERNAME_FIELD


class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "label"]
    ordering = ["verbose_name"]


class GrantAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "start", "end"]
    list_filter = ["start", "end"]
    ordering = ["-start"]
    raw_id_fields = ["grantor", "grantee"]
    search_fields = [
        "grantor__{username}".format(username=username_field),
        "grantee__{username}".format(username=username_field),
    ]


admin.site.register(Grant, GrantAdmin)
admin.site.register(Privilege, PrivilegeAdmin)
