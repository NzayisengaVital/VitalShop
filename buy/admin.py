from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'available',
        'created_at',
    )

    list_filter = (
        'category',
        'available',
    )

    search_fields = (
        'name',
        'description',
    )

    list_editable = (
        'price',
        'stock',
        'available',
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    extra = 0

    readonly_fields = (
        'product',
        'quantity',
        'price',
        'subtotal',
    )

    fields = (
        'product',
        'quantity',
        'price',
        'subtotal',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'phone',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone',
        'email',
    )

    readonly_fields = (
        'created_at',
        'total_amount',
    )

    list_editable = (
        'status',
    )

    inlines = [
        OrderItemInline,
    ]

    ordering = (
        '-created_at',
    )

    @admin.display(description='Customer')
    def customer_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'product',
        'quantity',
        'price',
        'subtotal',
    )

    search_fields = (
        'product__name',
        'order__first_name',
        'order__last_name',
    )

    readonly_fields = (
        'subtotal',
    )
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'subject',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'subject',
        'message',
    )

    ordering = ('-created_at',)
