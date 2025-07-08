from django.contrib import admin
from .models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trade model.
    """
    list_display = ['symbol', 'trade_type', 'quantity', 'price', 'total_value', 'trade_date']
    list_filter = ['trade_type', 'symbol', 'trade_date']
    search_fields = ['symbol', 'notes']
    readonly_fields = ['total_value', 'trade_date']
    ordering = ['-trade_date']
    
    fieldsets = (
        ('Trade Information', {
            'fields': ('symbol', 'trade_type', 'quantity', 'price')
        }),
        ('Additional Information', {
            'fields': ('notes', 'trade_date', 'total_value'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset for admin."""
        return super().get_queryset(request).select_related() 