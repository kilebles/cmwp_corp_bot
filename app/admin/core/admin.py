from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import Content, MenuButton, User, Mailing, MailingSend, ButtonClick, Section
from app.cmwp_corp_bot.services.broadcast_service import send_broadcast_by_id


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("slug", "preview", "media_kind", "media_url", "created_at")
    search_fields = ("slug", "text")
    list_filter = ("media_kind", "created_at")
    ordering = ("-created_at",)

    @admin.display(description=_("Контент"), ordering="text")
    def preview(self, obj):
        return (obj.text[:60] + "…") if obj.text and len(obj.text) > 60 else obj.text or "—"


class SegmentDetailInline(admin.TabularInline):
    model = MenuButton
    fk_name = "parent"
    extra = 1
    fields = ("label", "order", "link_url", "is_active")
    readonly_fields = ("is_active",)
    verbose_name = "Год"
    verbose_name_plural = "Обзоры по годам"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(section="SEGMENT_DETAIL")
    

@admin.register(MenuButton)
class MenuButtonAdmin(admin.ModelAdmin):
    list_display = ("section", "order", "label", "media_kind", "media_url", "link_url", "is_active")
    list_editable = ("order",)
    list_filter = ("section", "media_kind", "is_active")
    search_fields = ("label", "callback", "description")
    ordering = ("section", "order")
    readonly_fields = ("callback", "is_active", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("section", "order", "label", "parent")}),
        (_("Контент"), {"fields": ("description", "media_kind", "media_url", "link_url")}),
        (_("Системное"), {"fields": ("callback", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    inlines = [SegmentDetailInline]

    def get_inline_instances(self, request, obj=None):
        if obj and obj.section == "SEGMENT":
            return super().get_inline_instances(request, obj)
        return []


class ButtonClickInline(admin.TabularInline):
    model = ButtonClick
    extra = 0
    can_delete = False
    ordering = ("-ts",)

    fields = ("button_label", "section", "ts")
    readonly_fields = fields

    @admin.display(description="Кнопка")
    def button_label(self, obj: ButtonClick) -> str:
        return obj.button.label

    @admin.display(description="Раздел")
    def section(self, obj: ButtonClick) -> str:
        return obj.button.get_section_display()
    
    
class ClickedSectionFilter(SimpleListFilter):
    title = "Заходил в раздел"
    parameter_name = "clicked_section"

    def lookups(self, request, model_admin):
        return Section.choices

    def queryset(self, request, qs):
        if self.value():
            return qs.filter(clicks__button__section=self.value()).distinct()
        return qs


class ClickedButtonFilter(SimpleListFilter):
    title = "Нажимал кнопку"
    parameter_name = "clicked_button"

    def lookups(self, request, model_admin):
        return [(b.id, b.label) for b in MenuButton.objects.order_by("label")]

    def queryset(self, request, qs):
        if self.value():
            return qs.filter(clicks__button_id=self.value()).distinct()
        return qs


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "position",
                    "email", "phone", "created_at")
    search_fields = ("full_name", "company", "position",
                     "email", "phone")
    ordering = ("-created_at",)

    list_filter = (ClickedSectionFilter, ClickedButtonFilter)

    inlines = (ButtonClickInline,)


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
    actions = ["send_mailing"]

    @admin.display(description=_("Сообщение"))
    def preview(self, obj):
        txt = obj.text or "—"
        return (txt[:60] + "…") if len(txt) > 60 else txt

    @admin.action(description=_("Отправить выбранные рассылки"))
    def send_mailing(self, request, queryset):
        for mailing in queryset:
            try:
                send_broadcast_by_id(mailing.id)
                self.message_user(
                    request,
                    _(f"Рассылка {mailing.id} отправлена."),
                    messages.SUCCESS,
                )
            except Exception as exc:
                self.message_user(
                    request,
                    _(f"Ошибка в рассылке {mailing.id}: {exc}"),
                    messages.ERROR,
                )
    

from django.contrib.auth.models import Group, User as AuthUser
admin.site.unregister(Group)
admin.site.unregister(AuthUser)

admin.site.site_header = "CMWP-Bot Admin"
admin.site.index_title = "CMWP-Bot — управление"
admin.site.site_title = "CMWP-Bot Admin"