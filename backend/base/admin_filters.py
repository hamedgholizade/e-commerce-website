from django.contrib.admin import SimpleListFilter


class IsDeletedFilter(SimpleListFilter):
    """
    Filter for deleted items in the admin interface.
    """
    title = 'Deleted status'
    parameter_name = 'is_deleted'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Deleted'),
            ('no', 'Active'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(removed_at__isnull=False)
        if self.value() == 'no':
            return queryset.filter(removed_at__isnull=True)
        return queryset
