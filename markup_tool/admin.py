from django.contrib import admin
from markup_tool.models import Object, Classification, MarkingTask
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.unregister(Group)


class MarkingTaskInline(admin.TabularInline):
    model = MarkingTask
    fields = ('user', 'object', 'classification')

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyUserAdmin(UserAdmin):
    fieldsets = ((None, {"fields": ("username", "password")}), (_("Permissions"), {"fields": ("is_active", "is_superuser",)}))
    list_display = ['username', 'is_active', 'is_superuser']
    list_filter = []
    inlines = [MarkingTaskInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class ObjectAdmin(admin.ModelAdmin):
    fields = ['thumbnail_preview', 'image', 'marked']
    list_display = ['thumbnail_preview', 'marked']
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Preview'
    thumbnail_preview.allow_tags = True


admin.site.register(Object, ObjectAdmin)


class ClassificationAdmin(admin.ModelAdmin):
    fields = ('title',)


admin.site.register(Classification, ClassificationAdmin)


class MarkingTaskAdmin(admin.ModelAdmin):
    fields = ('user', 'object', 'classification')

    def delete_queryset(self, request, queryset):
        for q in queryset:
            q.object.marked = False
            q.object.save()
        super(MarkingTaskAdmin, self).delete_queryset(request, queryset)


admin.site.register(MarkingTask, MarkingTaskAdmin)
