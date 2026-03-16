from django.contrib import admin
from . import models


# Register your models here.
class PlayerCardAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("name", "team", "is_collected", "duplicate_count")
    list_filter = ("team", "is_collected")
    search_fields = ("name", "team__name")


admin.site.register(models.Team)
admin.site.register(models.PlayerCard, PlayerCardAdmin)
