from django.contrib import admin

from .models import Facemash

@admin.register(Facemash)
class FacemashAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'vk_id']
    list_display = ['first_name', 'last_name', 'vk_id', 'admin_image_thumb']