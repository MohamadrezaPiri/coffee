from django.contrib import admin
from django.db.models import Count

class ItemsCountFilter(admin.SimpleListFilter):
    title = 'Items count'
    parameter_name = 'items'

    def lookups(self, request, model_admin):
        return [
            ('=0', 'Without item'),
            ('>0', 'includes item')

        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(items_count=Count('items'))
        if self.value() == '=0':
            return annotated_value.filter(items_count=0)
        elif self.value() == '>0':
            return annotated_value.filter(items_count__gt=0)


class OrderDetailQuantityFilter(admin.SimpleListFilter):
    title = 'Quantity'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('=1', 'One Item'),
            ('>1', 'More than one')

        ]

    def queryset(self, request, queryset):
        if self.value() == '=1':
            return queryset.filter(quantity=1)
        elif self.value() == '>1':
            return queryset.filter(quantity__gt=1)


class OrderedTimesFilter(admin.SimpleListFilter):
    title = 'Have been ordered'
    parameter_name = 'orderdetail'

    def lookups(self, request, model_admin):
        return [
            ('>0', 'Yes'),
            ('=0', 'No')
        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(ordered_times=Count('orderdetail'))
        if self.value() == '=0':
            return annotated_value.filter(items_count=0)
        elif self.value() == '>0':
            return annotated_value.filter(items_count__gt=0)


class TablesCountFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'table'

    def lookups(self, request, model_admin):
        return [
            ('>0', 'Have table'),
            ('=0', 'Empty')
        ]

    def queryset(self, request, queryset):
        annotated_value=queryset.annotate(tables_count=Count('table'))
        if self.value() == '>0':
            return annotated_value.filter(tables_count__gt=0)
        elif self.value() == '=0':
            return annotated_value.filter(tables_count=0)   