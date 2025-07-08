from django.contrib import admin
from base.admin_filters import IsDeletedFilter


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for the application.
    This class can be extended by other admin classes to inherit common functionality.
    """
    date_hierarchy = "updated_at"
    list_per_page = 15
    readonly_fields = ['created_at', 'updated_at']
    list_filter = [IsDeletedFilter]
    
    def get_queryset(self, request):
        """
        User all_objects if the model has it, otherwise use the default queryset.
        """
        try:
            return self.model.all_objects.all()
        except AttributeError:
            return super().get_queryset(request)
    
    @admin.action(description='Soft delete selected items')
    def soft_delete(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()
        self.message_user(request, "Selected items have been soft deleted.")
    
    @admin.action(description='Hard delete selected items')
    def hard_delete(self, request, queryset):
        for obj in queryset:
            obj.hard_delete()
        self.message_user(request, "Selected items have been hard deleted.")
    
    @admin.action(description='Restore selected items')
    def restore(self, request, queryset):
        for obj in queryset:
            obj.restore()
        self.message_user(request, "Selected items have been restored.")

    actions = [soft_delete, hard_delete, restore]
