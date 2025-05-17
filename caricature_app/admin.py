from django.contrib import admin
from .models import StyleImage

# Register your models here.

@admin.register(StyleImage)
class StyleImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StyleImage._meta.fields]