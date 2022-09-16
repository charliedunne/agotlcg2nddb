from django.contrib import admin

from . import models

# Register your models here.
class CardAdmin(admin.ModelAdmin):
    list_display = ("code", "name")

class CycleAdmin(admin.ModelAdmin):
    list_display = ("short", "name")

class PackAdmin(admin.ModelAdmin):
    list_display = ("short", "name")

admin.site.register(models.Cycle, CycleAdmin)
admin.site.register(models.Pack, PackAdmin)
admin.site.register(models.Faction)
admin.site.register(models.Trait)
admin.site.register(models.Type)
admin.site.register(models.Card, CardAdmin)