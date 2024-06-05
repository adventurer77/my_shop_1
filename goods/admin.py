from django.contrib import admin
from goods.models import Categories,Products
from django.utils.safestring import mark_safe
# Register your models here.


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id","name","slug","is_visible", "sort")
    list_editable = ("name","slug","is_visible", "sort")
    list_filter = ("is_visible",)
    search_fields = ("name",)
    prepopulated_fields = {"slug" : ("name",)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("photo_src_tag","name","slug","description","price","discount","quantity","is_visible")
    list_editable = ("price","discount","quantity","is_visible")
    list_filter = ("category", "is_visible")
    search_fields = ("name",)
    prepopulated_fields = {"slug" : ("name",)}


    def photo_src_tag(self,obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50 height=50>")
        
    photo_src_tag.short_description = "Product photo"
    