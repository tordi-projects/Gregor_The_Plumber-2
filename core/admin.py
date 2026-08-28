from django.contrib import admin
from .models import Service, Testimonial, QuoteRequest


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'price_from', 'is_emergency', 'order')
    list_editable = ('order', 'is_emergency')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'location', 'rating', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_featured')
    search_fields = ('customer_name', 'comment')


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service', 'phone', 'is_emergency', 'status', 'whatsapp_notified', 'created_at')
    list_filter = ('status', 'is_emergency', 'whatsapp_notified', 'service')
    search_fields = ('full_name', 'email', 'phone', 'address')
    readonly_fields = ('created_at', 'whatsapp_notified')
