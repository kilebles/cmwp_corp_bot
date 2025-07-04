from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Content, MenuButton, User, Mailing, MailingSend


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("slug", "preview", "media_kind", "media_url", "created_at")
    search_fields = ("slug", "text")
    list_filter = ("media_kind", "created_at")
    ordering = ("-created_at",)

    @admin.display(description=_("Контент"), ordering="text")
    def preview(self, obj):
        return (obj.text[:60] + "…") if obj.text and len(obj.text) > 60 else obj.text or "—"


@admin.register(MenuButton)
class MenuButtonAdmin(admin.ModelAdmin):
    list_display = ("section", "order", "label", "media_kind", "media_url", "link_url", "is_active")
    list_editable = ("order",)                                 # ← is_active убрали
    list_filter = ("section", "media_kind", "is_active")
    search_fields = ("label", "callback", "description")
    ordering = ("section", "order")
    readonly_fields = ("callback", "is_active", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("section", "order", "label")}),
        (_("Контент"), {"fields": ("description", "media_kind", "media_url", "link_url")}),
        (_("Системное"), {"fields": ("callback", "created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "position", "email", "phone", "created_at")
    search_fields = ("full_name", "company", "position", "email", "phone")
    ordering = ("-created_at",)


class MailingSendInline(admin.TabularInline):
    model = MailingSend
    extra = 0
    readonly_fields = ("user", "status", "ts")
    can_delete = False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "media_kind", "preview")
    ordering = ("-created_at",)
    inlines = (MailingSendInline,)

    @admin.display(description=_("Сообщение"))
    def preview(self, obj):
        return (obj.text[:60] + "…") if obj.text and len(obj.text) > 60 else obj.text or "—"


from django.contrib.auth.models import Group, User as AuthUser
admin.site.unregister(Group)
admin.site.unregister(AuthUser)

admin.site.site_header = "CMWP-Bot Admin"
admin.site.index_title = "CMWP-Bot — управление"
admin.site.site_title = "CMWP-Bot Admin"