from django.contrib import admin, messages

from justsite.models import Items, TagItem, Category, Comments, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'time_create', 'price', 'rate')
    ordering = ['-time_create', 'name']
    actions = ['set_published', 'set_draft']
    list_editable = ('is_published',)
    # поиск независимо от регистра
    search_fields = ('name__icontains', )
    list_filter = ['cat__name', 'is_published', 'tags']


    @admin.action(description="Добавить товары на витрину")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Items.Status.PUBLISHED)
        self.message_user(request, f"{count} товаров выставлено на витрину")

    @admin.action(description="Снять товары с витрины")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Items.Status.DRAFT)
        self.message_user(request, f"{count} товаров снято с витрины", messages.WARNING)



class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'text', 'time_create')
    list_display_links = ('text', )
    readonly_fields = ['user', 'item', 'text', 'rating']
    search_fields = ('text__icontains',)



class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    fields = ['user', 'time_create', 'status', 'order_sum']
    list_display = ('user', 'time_create', 'status', 'order_sum')
    list_display_links = ('time_create', )
    readonly_fields = ['user', 'time_create', 'order_sum']
    list_editable = ('status',)

    actions = ['set_on_the_job', 'set_ready_to_go', 'set_finished']

    @admin.action(description="Перевести заказы на статус 'В работе'")
    def set_on_the_job(self, request, queryset):
        count = queryset.update(status=Order.Status.ONTHEJOB)
        self.message_user(request, f"{count} заказов переведено в статус 'В работе'")

    @admin.action(description="Перевести заказы на статус 'Готов к выдаче'")
    def set_ready_to_go(self, request, queryset):
        count = queryset.update(status=Order.Status.READYTOGO)
        self.message_user(request, f"{count} заказов переведено в статус 'Готов к выдаче'")

    @admin.action(description="Перевести заказы на статус 'Выдан'")
    def set_finished(self, request, queryset):
        count = queryset.update(status=Order.Status.FINISHED)
        self.message_user(request, f"{count} заказов переведено в статус 'Выдан'")



admin.site.register(Items, ItemsAdmin)
admin.site.register(TagItem)
admin.site.register(Category)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Order, OrderAdmin)
