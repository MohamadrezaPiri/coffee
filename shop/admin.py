from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import urlencode, format_html
from django.db.models import Count
from .models import Category, Items, Order, Hall, Table, OrderDetail
from .filters import ItemsCountFilter, OrderDetailQuantityFilter, TablesCountFilter

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['title', 'items_count']
    list_filter = [ItemsCountFilter]
    search_fields = ['title']
    actions = ['clear_items']

    @admin.display(ordering='items_count')
    def items_count(self, category):
        url = (
            reverse('admin:shop_items_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        
        if category.items_count in [0,1]:
            return format_html('<a href="{}">{} Item</a>', url, category.items_count)
        return format_html('<a href="{}">{} Items</a>', url, category.items_count)

    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('items')
        )
    
    @admin.action(description='Clear Items')
    def clear_items(self, request, queryset):
        total_items_count = sum(category.items.count() for category in queryset)

        for category in queryset:
            category.items.all().delete()

        self.message_user(
            request,
            f'{total_items_count} items removed',
            messages.SUCCESS
        )    

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ['name','price','category','ordered_times']
    list_filter = ['category']
    search_fields = ['name']
    autocomplete_fields = ['category']

    @admin.display(ordering='ordered_times')
    def ordered_times(self, item):
        return item.ordered_times

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            ordered_times=Count('orderdetail'),
        )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderid','table','total_price','payment_status']
    search_fields = ['orderid']
    autocomplete_fields = ['table']

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'tables_count']
    list_filter = [TablesCountFilter]
    search_fields = ['name']
    actions = ['clear_tables']

    @admin.display(ordering='tables_count')
    def tables_count(self, hall):
        url = (
            reverse('admin:shop_table_changelist')
            + '?'
            + urlencode({
                'hall__id': str(hall.id)
            }))
        
        if hall.tables_count in [0,1]:
            return format_html('<a href="{}">{} Table</a>', url, hall.tables_count)
        return format_html('<a href="{}">{} Tables</a>', url, hall.tables_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tables_count=Count('table')
        )
    
    @admin.action(description='Clear Tables')
    def clear_tables(self, request, queryset):
        total_tables_count = sum(hall.table_set.count() for hall in queryset)

        for hall in queryset:
            hall.table_set.all().delete()

        self.message_user(
            request,
            f'{total_tables_count} tables removed',
            messages.SUCCESS
        )    

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['name','hall','is_free']    
    list_filter = ['hall__name']
    list_editable = ['is_free']
    search_fields = ['name']
    autocomplete_fields = ['hall']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order','item','quantity','price']
    list_filter = ['order', OrderDetailQuantityFilter]
    autocomplete_fields = ['item','order']
    search_fields = ['item__name']