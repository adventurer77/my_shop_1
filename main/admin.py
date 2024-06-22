from django.contrib import admin
from main.models import Contact

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id","name","email","phone", "comment","is_confirmed","date_created","date_updated")
    list_editable = ("name","email","phone", "comment","is_confirmed")
    list_filter = ("date_created",)
    search_fields = ("name","email","phone")

# admin.site.register(Contact)