from django.contrib.admin import SimpleListFilter


class IsActiveFilter(SimpleListFilter):
    """
    Filter for deleted items in the admin interface.
    """
    title = 'Active status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Active'),
            ('no', 'Removed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_active=True)
        if self.value() == 'no':
            return queryset.filter(is_active=False)
        return queryset
